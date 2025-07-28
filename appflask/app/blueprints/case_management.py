import os
import pdfkit
from datetime import date, datetime
from pathlib import Path

import click
import pypdftk
from PyPDF2 import PdfFileMerger
from flask import Blueprint, render_template
from flask_security import login_required
from tqdm import tqdm

from app.case_management.services import CaseService, EvidenceService
from app.data_import.hearing.hearing import HearingProcessor
from app.database.models import Files
from app.pdf.sign_pdf import sign_pdf

from app import db
from app.case_management.models import NoteSender, Note, Application, CaseProperty, NoteDescription, NoteType, Client
from app.database.models.user import Permission
from app.email import send_email, EmailTuple, EmailToClient
from app.evidence.evidence_document import EvidenceDocument
from app.routing.services import ScraperService, ReportService, PetitionsReportService
from app.settings.models import GlobalSetting
from app.singlecma.models import SingleCMAWorkups, SingleCMAWorkupsSchema
from app.utils.constants import County
from config import APP_ROOT, EVIDENCE_DIR, DATA_IMPORT

bp = Blueprint('case_management', __name__, url_prefix='/cases')


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@bp.route('/')
@login_required
def page():
    return render_template('case_management.html', items=None)


@bp.cli.command('truncate')
def truncate():
    """
    Truncate all dynamic data related to case manaagement
    """
    with db.engine.connect() as conn:
        conn.execute('''
        TRUNCATE TABLE case_property CASCADE;
        TRUNCATE TABLE case_note CASCADE;
        TRUNCATE TABLE case_email CASCADE;
        TRUNCATE TABLE case_client_tag CASCADE;
        TRUNCATE TABLE case_client CASCADE;
        TRUNCATE TABLE case_billing CASCADE;
        TRUNCATE TABLE case_application CASCADE;

        ALTER SEQUENCE case_property_id_seq RESTART;
        ALTER SEQUENCE case_note_id_seq RESTART;
        ALTER SEQUENCE case_email_id_seq RESTART;
        ALTER SEQUENCE case_client_id_seq RESTART;
        ALTER SEQUENCE case_billing_id_seq RESTART;
        ALTER SEQUENCE case_application_id_seq RESTART;
        ''')
    print('Tables truncated')
    return


@bp.cli.command('daily_email')
def daily_email():
    """
    Send daily email informing amount of new applications
    """
    latest_robot_note = Note.query.filter(Note.sender == NoteSender.ROBOT).order_by(Note.created_at.desc()).first()

    new_note = Note.create_note(
        sender=NoteSender.ROBOT,
        text="Daily email sent",
    )

    if not latest_robot_note:
        print('First robot note created...')
        new_applications_count = Application.query.count()
    else:
        new_applications_count = Application.query.filter(
            Application.created_at.between(latest_robot_note.created_at, new_note.created_at)).count()

    today = date.today().strftime('%m/%d/%Y')
    email = EmailTuple(title=f"Redux: Daily Report - {today}."
                             f" {new_applications_count} New Applications.",
                       template_path="email/daily_email")

    # retrieve recipients from database
    q = GlobalSetting.query.filter(GlobalSetting.county.is_(None)).first()
    recipients = q.settings['daily_emails']

    send_email(to=recipients, email_to_client=email, template_extension='.txt', today=today,
               new_applications_count=new_applications_count)

    print(f'sent mail to {recipients} on {today}')
    return


@bp.cli.command('merge_email_clients')
@click.argument('email_address')
@click.option('--drop_duplicated', is_flag=True)
def merge_email_clients(email_address, drop_duplicated):
    from app.case_management.services import CaseService
    CaseService.merge_email_clients(email_address, drop_duplicated)


@bp.cli.command('broward_evidence')
@click.argument('apn')
def broward_evidence(apn):
    ScraperService().broward_evidence(apn, gen_pdf=True, gen_html=False)


@bp.cli.command('miamidade_evidence')
@click.argument('apn')
def miamidade_evidence(apn):
    ScraperService().miamidade_evidence(apn, gen_pdf=True, gen_html=False)


@bp.cli.command('back_fill_contact_agreement')
def back_fill_contact_agreement():
    from app.case_management.services import CaseService
    CaseService.back_fill_contact_agreement()


@bp.cli.command('broward_evidence_package')
@click.argument('case_id')
def broward_evidence_package(case_id):
    """
    Generate broward evidence package
    """
    case = CaseProperty.get(case_id)
    prop = case.property
    apn = prop.apn

    template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'evid_template.docx'
    pet_evid_pdf_path = EvidenceDocument(template_path=template).gen_petition_document(case)

    try:
        # gen broward print pdf file
        ScraperService().broward_evidence(apn, gen_html=False, gen_pdf=True)
        print_pdf_path = (EVIDENCE_DIR / apn / f'{apn}.pdf').as_posix()
    except Exception as e:
        print(e.args)
        print_pdf_path = None

    workup = SingleCMAWorkups.get_last_workup(case_id)
    report_file_path = None
    if workup:
        data = workup.report_file.data
        if data:
            report_file_path = EVIDENCE_DIR / apn / f'cma_report_{apn}.pdf'

        if report_file_path:
            with open(report_file_path, 'wb') as w:
                w.write(data)

    merger = PdfFileMerger()
    merger.append(pet_evid_pdf_path)

    if print_pdf_path:
        merger.append(print_pdf_path)

    if report_file_path:
        merger.append(report_file_path.as_posix())

    merger.write((EVIDENCE_DIR / f'{apn}.pdf').as_posix())
    merger.close()


@bp.cli.command('miamidade_evidence_package')
@click.argument('case_id')
def miamidade_evidence_package(case_id):
    """
    Generate miamidade evidence package
    """
    case = CaseProperty.get(case_id)
    prop = case.property
    apn = prop.apn

    # generate pet evid pdf file
    template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'evid_template.docx'
    pet_evid_pdf_path = EvidenceDocument(template_path=template).gen_petition_document(case)

    try:
        # generate miamidade print pdf file
        ScraperService().miamidade_evidence(apn, gen_html=False, gen_pdf=True)
        print_pdf_path = (EVIDENCE_DIR / apn / f'{apn}.pdf').as_posix()
    except Exception as e:
        print(e.args)
        print_pdf_path = None

    # get last workup
    workup = SingleCMAWorkups.get_last_workup(case_id)
    report_file_path = None
    if workup:
        data = workup.report_file.data
        if data:
            report_file_path = EVIDENCE_DIR / apn / f'cma_report_{apn}.pdf'

        # generate report pdf file
        if report_file_path:
            with open(report_file_path, 'wb') as w:
                w.write(data)

    # merge files in one
    merger = PdfFileMerger()
    merger.append(pet_evid_pdf_path)

    if print_pdf_path:
        merger.append(print_pdf_path, pages=(0, 1))
    if report_file_path:
        merger.append(report_file_path.as_posix())

    merger.write((EVIDENCE_DIR / f'{apn}.pdf').as_posix())
    merger.close()


def helper_dr486_pdf_template(case):
    pdf_template = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'DR_486_sample.pdf'
    signature_path = Path(APP_ROOT) / 'app' / 'templates' / 'evidence' / 'Ron_Signature.png'
    # get property
    case_client = case.client

    context = {
        'Taxpayer name': case_client.full_name if case_client else '',
        'Date_3': datetime.now().strftime('%m/%d/%y'),
        'Mailing address for notices': '103-11 Metropolitan Ave, Forest Hills, NY 11375',
        'Parcel ID and physical address or TPP account': ', '.join([
            case.property.apn or '', case.property.address or ''
        ]).strip(', ')
    }
    form_filled_pdf = pypdftk.fill_form(pdf_path=pdf_template, datas=context)
    signed_pdf = sign_pdf(coords='2x150x98x93x27',
                          pdf=form_filled_pdf,
                          png_signature=signature_path,
                          signature=None)

    return signed_pdf


@bp.cli.command('dr486_pdf_template')
@click.argument('case_id')
def dr486_pdf_template(case_id):
    # get case object
    case = CaseProperty.get(case_id)

    return helper_dr486_pdf_template(case)


@bp.cli.command('submission_contracts_dr486')
@click.argument('county')
@click.argument('path')
@click.argument('tax_year')
@click.argument('property_type', required=False)
def submission_contracts_dr486(county, path, tax_year=2020, property_type=None):
    """
    path: specify path that will be created in appflask folder.
    ex. 'test_path/save_folder'
    """
    assert property_type in ['vacant', 'residential', 'condo', None]

    root_path = Path(APP_ROOT)

    # create directory where files to be stored
    os.makedirs(root_path / path, exist_ok=True)

    # create sub directory for dr486 reports
    dr_reports_path = root_path / path / 'dr486'
    os.makedirs(dr_reports_path, exist_ok=True)

    # create sub directry for signed_contracts
    signed_contracts_path = root_path / path / 'signed_contracts'
    os.makedirs(signed_contracts_path, exist_ok=True)

    query = CaseProperty.query.filter(CaseProperty.county == county,
                                      CaseProperty.tax_year == tax_year)

    cases = query.all()

    if property_type == 'vacant':
        cases = [c for c in cases if c.property.property_class == 0]
    elif property_type == 'condo':
        cases = [c for c in cases if c.property.is_condo is True]
    elif property_type == 'residential':
        cases = [c for c in cases
                 if c.property.property_class != 0 and c.property.is_condo is not True]
    else:
        pass

    if not cases:
        print('no cases found')

    pbar = tqdm(total=len(cases), desc='saving contracts')
    for case in cases:

        # save signed contracts
        pbar.update(1)
        if not case.application:
            print(f'case {case.id} missing application')
            continue
        notes = Note.get_contract_notes(case.application)

        if not notes or len(notes) > 1:
            # something does not match
            print(f'case {case.id} missing attachments or has more than one')
            continue
        attachment = notes[0].attachment

        if not attachment:
            print(f"The attachment file for the case with id={case.id} was not found")
            continue
        pdf = attachment.decode('utf-8').encode('latin-1')

        apn = case.application.apn if case.application else None
        if apn and case.county == County.MIAMIDADE:
            apn = '-'.join([apn[:2], apn[2:6], apn[6:9], apn[9:]])
        elif not apn:
            apn = f'case_{case.id}_missing_application_apn'

        with open(signed_contracts_path / f'{apn}.pdf', 'wb') as f:
            f.write(pdf)

        # save dr486 contracts
        pdf_path = helper_dr486_pdf_template(case)
        os.rename(pdf_path, dr_reports_path / f'{apn}.pdf')


@bp.cli.command('send_vab_emails')
@click.option('--txt-file', '-tf', type=click.Path())
def send_vab_emails(txt_file):
    """
    txt_file: input file containing case ids
    ex. /Users/iammashed/projects/globalcma/case_ids/case_ids.txt
    """
    with open(txt_file, 'r') as f:
        content = f.read()
    case_ids = content.strip('\n').split('\n')

    pbar = tqdm(case_ids, desc='Sending VAB emails...')
    for cid in case_ids:
        pbar.update(1)
        case = CaseProperty.get(cid)
        if not case.application:
            print(f'case {cid} missing application')
            continue
        email_context = CaseService.get_email_context(case.application)
        email = case.client.email.email_address if case.client and case.client.email else None
        if not email:
            print(f'case {cid} missing client email')

        email_to_client = EmailToClient.vab
        send_email(email,
                   email_to_client=email_to_client,
                   **email_context)

        html_string = render_template(email_to_client.template_path + '.html',
                                      **email_context)
        pdf_binary = pdfkit.from_string(html_string, False).decode(
            'ISO-8859-1').encode('utf-8')
        Note.create_system_note(NoteSender.CASE_PROPERTY,
                                case.application,
                                NoteDescription.CASE_VAB_EMAIL_SENT,
                                NoteType.EMAIL_SENT,
                                attachment=pdf_binary,
                                attachment_extension='.pdf'
                                )


@bp.cli.command('send_client_vab_emails')
@click.option('--txt-file', '-tf', type=click.Path())
@click.option('--testing', is_flag=True)
def send_client_vab_emails(txt_file, testing):
    """
    txt_file: input file containing client ids
    """
    with open(txt_file, 'r') as f:
        content = f.read()
    client_ids = content.strip('\n').split('\n')

    if testing:
        print('Testing mode')

    pbar = tqdm(client_ids, desc='Sending VAB emails...')
    for client_id in client_ids:
        pbar.update(1)
        client = Client.get(client_id)
        if client.type_id != Client.CURRENT:
            print(f'Error: Not current client {client.id}')
            continue

        addresses = client.get_cases_addresses()
        # email_context = CaseService.get_email_context(client.application)
        email_context = dict(
            full_name=client.full_name,
            addresses=addresses
        )

        email_address = client.email.email_address if client.email else None
        if not email_address:
            print(f'client {client_id} missing client email')

        # if testing is true, send test emails to test email list only
        # if testing and email_address and email_address not in CaseService.get_test_email_list():
        #     continue

        if testing and client.id not in [51, 26, 71]:
            continue

        email_to_client = EmailToClient.vab
        send_email(email_address,
                   email_to_client=email_to_client,
                   **email_context)
        print(f'email sent to: {email_address}')
        # print('client cases addresses:')
        # for addr in addresses:
        #     print(addr)

        html_string = render_template(email_to_client.template_path + '.html',
                                      **email_context)
        pdf_binary = pdfkit.from_string(html_string, False).decode(
            'ISO-8859-1').encode('utf-8')

        # log the client activity
        Note.create_system_note(NoteSender.CLIENT,
                                client,
                                NoteDescription.PETITION_SUBMITTED,
                                NoteType.EMAIL_SENT,
                                attachment=pdf_binary,
                                attachment_extension='.pdf'
                                )


@bp.cli.command('active_case_ids')
@click.option('--txt-file-path', '-tf', type=click.Path())
def active_case_ids(txt_file_path):
    file_name = 'active_case_ids.txt'
    if not os.path.exists(txt_file_path):
        os.makedirs(txt_file_path, exist_ok=True)
    file_path = os.path.join(txt_file_path, file_name)
    with open(file_path, 'w') as f:
        cases = db.session.query(CaseProperty.id).all()
        f.write('\r\n'.join([str(c[0]) for c in cases]))
    print(f'File saved at {file_path}')


@bp.cli.command('active_client_ids')
@click.option('--txt-file-path', '-tf', type=click.Path())
def active_client_ids(txt_file_path):
    file_name = 'active_client_ids.txt'
    if not os.path.exists(txt_file_path):
        os.makedirs(txt_file_path, exist_ok=True)
    file_path = os.path.join(txt_file_path, file_name)
    with open(file_path, 'w') as f:
        clients = db.session.query(Client.id).filter(Client.type_id == Client.CURRENT).all()
        f.write('\r\n'.join([str(c[0]) for c in clients]))
    print(f'File saved at {file_path}')


@bp.cli.command('gen_cover_page')
@click.argument('case_id')
def gen_cover_page(case_id):
    """
    Generate cover page required for evidence package document
    """
    case = CaseProperty.get(case_id)

    # we can't generate a document if case object is wrong or case property is not found skip this case
    if case and case.property:
        data = dict(
            petition_number='2019-222222',
            hearing_date='15/10/2019',
            hearing_time=datetime.now().strftime('%I:%M%p').lstrip('0'),
            board_room='13',
            current_market_value=ReportService.format_price(123456),
            proposed_market_value=ReportService.format_price(123456)
        )
        EvidenceService().gen_cover_page(case, **data)


@bp.cli.command('download_workup_file')
@click.argument('file_id')
def download_workup_file(file_id):
    """
    Download workup cma report pdf file
    """
    file = Files.get(file_id)
    data = file.data
    if data:
        report_file_path = EVIDENCE_DIR / f'cma_report_{file.name}'

        # generate report pdf file
        if report_file_path:
            with open(report_file_path, 'wb') as w:
                w.write(data)


@bp.cli.command('download_application_scan')
@click.argument('case_id')
def download_application_scan(case_id):
    """
    Download application submission pdf file
    """
    case = CaseProperty.get(case_id)
    EvidenceService().gen_application_submission(case)


@bp.cli.command('gen_case_evidence_package')
@click.argument('case_id')
def gen_case_evidence_package(case_id):
    """
    Download application submission pdf file
    """
    case = CaseProperty.get(case_id)
    EvidenceService().gen_evidence_package(case)


@bp.cli.command('update_case_hearing_data')
def update_case_hearing_data():
    """
    Update existed or insert new case hearing data
    """
    # HearingProcessor(
    #     'Scheduled Hearing Dates.xlsx',
    #     parse_row_func=HearingProcessor.parse_scheduled_hearing_dates
    # ).process(
    #     skiprows=13,
    #     usecols="C:G",
    #     dtype={
    #         "Parcel #": str,
    #         "Hearing Date/Time": str,
    #         "Room": str,
    #         "Petition #": str
    #     }
    # )

    HearingProcessor(
        'hearing info (2).xlsx',
        parse_row_func=HearingProcessor.parse_hearing_info
    ).process(
        usecols="A:F",
        dtype={
            "Folio": str,
            "Hearing Date/Time": str,
            "Room": str,
            "Petition #": str
        }
    )

    # HearingProcessor(
    #     '2020 Petition - Redux.xls',
    #     parse_row_func=HearingProcessor.parse_petition_redux
    # ).process(
    #     usecols=['PetitionNumber', 'Parcel ID', 'DOR', 'HearingDate'],
    #     dtype={
    #         "PetitionNumber": object,
    #         "HearingDate": datetime,
    #         "DOR": object,
    #         "Parcel ID": object
    #     }
    # )


@bp.cli.command('insert_workup')
def insert_workup():
    import json
    with open(DATA_IMPORT / '30.txt') as json_file:
        cma_payload = json.load(json_file)

        json_data = {
            'report_file_id': 30,
            'good_bad_report_file_id': None,
            'created_at': '2020-10-06 18:49:06.536677',
            'cma_payload': cma_payload,
            'is_primary': False,
            'case_property_id': 89
        }

        new_workup = SingleCMAWorkupsSchema().load(json_data)
        new_workup.save()


@bp.cli.command('create_petitions_template')
@click.argument('rows_count')
def create_petitions_template(rows_count):
    # dummy data
    rows = (
        ('474131AA0410', '2020-11111', 297890, 274478, 277854, 274478),
        ('494122271030', '2020-17717', 142180, 148822, 125562, 133990),
        ('494126040270', '2020-17718', 182680, 197086, 160842, 178610),
        ('494127261910', '2020-17720', 202110, 222191, 196051, 201860),
        ('494131182920', '2020-17721', 385380, 342425, 342425, 385380),
        ('494135130020', '2020-17722', 201600, '', '', 201600),
    )

    service = PetitionsReportService()
    service.insert_summary_worksheet_rows(rows)
    service.setup_summary_worksheet()
    service.workbook.save(DATA_IMPORT / 'petitions_template.xlsx')
