import ftplib
import os
from pathlib import Path
from zipfile import ZipFile

import click
import wget
from flask import Blueprint, current_app
from scourgify.normalize import normalize_addr_str
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from tqdm import tqdm

from app import photos, db
from app.data_import.broward.assessment import BrowardAssessmentProcessor
from app.data_import.broward.owner import BrowardPropertyOwnerProcessor, BrowardAssessmentOwnerProcessor
from app.data_import.broward.property import BrowardPropertyProcessor, BrowardGISProcessor, BrowardPoolProcessor, \
    BrowardCondosProcessor
from app.data_import.florida import FloridaObsolescenceProcessor, FloridaSaleProcessor, FloridaUnitProcessor, \
    FloridaOwnerStateProcessor
from app.data_import.miamidade.assessment import MiamidadeAssessmentProcessor, MiamidadeRollProcessor, \
    MiamidadeCompareAssessments
from app.data_import.miamidade.owner import MiamidadePropertyOwnerProcessor, MiamidadeAssessmentOwnerProcessor
from app.data_import.miamidade.property import MiamidadePropertyProcessor, MiamidadeGISProcessor, \
    MiamidadeLandTypeCodeProcessor, MiamidadePoolProcessor, MiamidadeCondoCodesProcessor, \
    MiamidadeInventoryUpdateProcessor
from app.data_import.nassau.assessment import NassauAssessmentProcessor
from app.data_import.nassau.property import process_input_file, NassauGISProcessor
from app.data_import.nassau.sale import NassauCUWSaleProcessor, NassauSaleFileProcessor
from app.data_import.palmbeach.assessment import PalmbeachAssessmentProcessor
from app.data_import.palmbeach.owner import PalmbeachPropertyOwnerProcessor, PalmbeachAssessmentOwnerProcessor
from app.data_import.palmbeach.property import PalmbeachPropertyProcessor, PalmbeachGISProcessor
from app.data_import.suffolk.assessment import Processor as SuffolkAP
from app.data_import.suffolk.owner import OwnerProcessor
from app.data_import.suffolk.property import SuffolkGISProcessor, SuffolkPropertyProcessor
from app.data_import.processor import ProcessorOperation, ProcessorSettings
from app.data_import.suffolk.sale import SuffolkSaleFileProcessor
from app.database.models import Property, PropertyPhoto
from app.utils.address_utils import AddressUnitParser
from app.utils.constants import County, extract_date_from_photo_name
from app.utils.fix_address import FixAddress, CapitalizeAddress
from app.utils.gis_utils import GeometryProcessor
from app.utils.number_converter import mask_to_dec, dec_to_base, base_to_dec
from config import DATA_IMPORT, SQLALCHEMY_DATABASE_URI
from my_logger import logger

bp = Blueprint('fill_sample', __name__)


@bp.cli.command('nassau')
@click.argument('table')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.option('--owner', is_flag=True)
def nassau(table, csv, persist, owner):
    """Fill database with Nassau input source"""
    if table == 'property':
        process_input_file('commercial.asc', persist=persist, csv=csv)
    elif table == 'gis':
        NassauGISProcessor(persist=persist, to_file=csv).process_gis()
    elif table == 'assessment':
        NassauAssessmentProcessor(
            'tent_2021',
            assessment_type_id=2,
            assessment_date_id=13,
            to_file=csv,
            persist=persist,
            drop_imported=True
        ).process_dir(operation=ProcessorOperation.INSERT)

        # processor.process_input_folder(csv, persist)
    elif table == 'sale':
        # nassau_sale_processor = SaleProcessor('nassau',
        #                                       '2816_CUR.CSV',
        #                                       schema=NassauSaleSchema,
        #                                       to_csv=csv,
        #                                       persist=persist,
        #                                       owner=owner)
        # nassau_sale_processor.process_input_file()
        NassauSaleFileProcessor(
            file_name='NASS_sale.txt',
            persist=persist,
            csv=csv
        ).process_file()
    elif table == 'cuw':
        NassauCUWSaleProcessor(file_name='NASS_CUW.txt', persist=persist, to_file=csv, owner=owner).process_input_file()
    else:
        print('invalid county or table names')


@bp.cli.command('suffolk')
@click.argument('table')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.option('--drop_imported', is_flag=True)
def suffolk(table, persist, csv, drop_imported):
    """
    Process Suffolk county:
    Possible 'table' attribute values:
        - property
        - gis
        - sale
        - assessment
    """
    if table == 'property':
        processor_settings = ProcessorSettings(
            persist=persist,
            to_file=csv,
            operation=ProcessorOperation.UPDATE,
            persist_validation_errors=False,
            drop_imported=drop_imported
        )
        SuffolkPropertyProcessor(settings=processor_settings).process()

    elif table == 'gis':
        SuffolkGISProcessor(file_name='Land_Use_-_2016-shp.zip', persist=persist, to_file=csv).process_gis_zip()
    elif table == 'sale':
        # proc = SuffolkSaleProcessor(county='suffolk',
        #                             file_name='4716_CUR.CSV',
        #                             schema=SaleSchema,
        #                             to_csv=csv,
        #                             persist=persist,
        #                             owner=owner)
        # proc.process_input_file()
        SuffolkSaleFileProcessor(
            file_name='dbo_Suffolk Sales VTable.txt',
            persist=persist,
            csv=csv
        ).process_file()
    elif table == 'assessment':
        SuffolkAP(
            'suffolk', persist=persist,
            csv_output=csv,
            app=current_app._get_current_object()).process_input_file()
    elif table == 'owner':
        OwnerProcessor('suffolk',
                       persist=persist,
                       csv_output=csv,
                       app=current_app._get_current_object()).process_input_file()
    else:
        print('invalid command')


@bp.cli.command('broward')
@click.argument('table')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def broward(table, persist, csv):
    if table == 'property':
        BrowardPropertyProcessor(file_name='BCPA_TAX_ROLL.csv', persist=persist, to_file=csv).process_input_file()
    elif table == 'gis':
        BrowardGISProcessor(file_name='BCPA_GIS_LABEL.zip', persist=persist, to_file=csv).process_gis()
    elif table == 'owner':
        # process owner from property data
        BrowardPropertyOwnerProcessor(
            file_name='BCPA_TAX_ROLL.csv',
            persist=persist,
            to_file=csv
        ).process_owner()

        # process owner from assessment data
        BrowardAssessmentOwnerProcessor(
            nap_file_name='NAP16F201901.csv',
            nal_file_name='NAL16F201901.csv',
            persist=persist,
            to_csv=csv
        ).process_owner()

    elif table == 'assessment':
        BrowardAssessmentProcessor(
            nap_file_name='NAP16F201901.csv',
            nal_file_name='NAL16F201901.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'sale':
        FloridaSaleProcessor(
            provider_name=County.BROWARD,
            file_name='SDF16F201901.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'obsolescence':
        # store 'broward' land use codes from assessment source file to property table
        FloridaObsolescenceProcessor(
            provider_name=County.BROWARD,
            persist=persist,
            to_file=csv
        ).process_input_file()
    else:
        print('Invalid table name')


@bp.cli.command('palmbeach')
@click.argument('table')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def palmbeach(table, persist, csv):
    if table == 'property':
        PalmbeachPropertyProcessor(
            file_name='PAS405_CERT2019_20191017.TXT',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'gis':
        PalmbeachGISProcessor(file_name='PARCELS.zip', persist=persist, to_file=csv).process_gis()
    elif table == 'assessment':
        PalmbeachAssessmentProcessor(
            nap_file_name='NAP60F201901.csv',
            nal_file_name='NAL60F201902.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'sale':
        FloridaSaleProcessor(
            provider_name=County.PALMBEACH,
            file_name='SDF60F201902.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'owner':
        # process owner info from property data
        PalmbeachPropertyOwnerProcessor(
            file_name='OWNER_PAS405_CERT2019_20191017.csv',
            persist=persist,
            to_file=csv
        ).process_owner()

        # process owner info from assessment data
        PalmbeachAssessmentOwnerProcessor(
            nap_file_name='NAP60F201901.csv',
            nal_file_name='NAL60F201902.csv',
            persist=persist,
            to_csv=csv
        ).process_owner()
    elif table == 'obsolescence':
        # store 'palmbeach' land use codes from assessment source file to property table
        FloridaObsolescenceProcessor(
            provider_name=County.PALMBEACH,
            persist=persist,
            to_file=csv
        ).process_input_file()
    else:
        print('Invalid table name')


@bp.cli.command('miamidade')
@click.argument('table')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def miamidade(table, persist, csv):
    if table == 'property':
        MiamidadePropertyProcessor(
            file_name='MunRoll - 00 RE - All Properties.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'gis':
        MiamidadeGISProcessor(file_name='Property_Boundary_View.csv', persist=persist, to_file=csv).process_gis()
    elif table == 'owner':
        MiamidadePropertyOwnerProcessor(
            file_name='MunRoll - 00 RE - All Properties.csv',
            persist=persist,
            data_source='property',
            to_file=csv
        ).process_owner()

        MiamidadeAssessmentOwnerProcessor(
            nap_file_name='NAP23F201901.csv',
            nal_file_name='NAL23F201901.csv',
            persist=persist,
            to_csv=csv
        ).process_owner()
    elif table == 'assessment':
        MiamidadeAssessmentProcessor(
            nap_file_name='NAP23F201901.csv',
            nal_file_name='NAL23F201901.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'sale':
        FloridaSaleProcessor(
            provider_name=County.MIAMIDADE,
            file_name='SDF23F201901.csv',
            persist=persist,
            to_file=csv
        ).process_input_file()
    elif table == 'obsolescence':
        # store 'miamidade' land use codes from assessment source file to property table
        FloridaObsolescenceProcessor(
            provider_name=County.MIAMIDADE,
            persist=persist,
            to_file=csv
        ).process_input_file()
    else:
        raise Exception('Invalid table name')


@bp.cli.command('property_unit')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def property_unit(persist, csv):
    """
    Parse Florida unit numbers (flats) and store into property table
    """
    for county in County.get_florida_counties():
        print('Start parsing units of {} county'.format(county))
        FloridaUnitProcessor(county, persist, csv).process_file()
        print('End parsing for {} county'.format(county))


@bp.cli.command('parse_owner_mailing_state')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def parse_owner_mailing_state(persist, csv):
    """
    Parse owner mailing state for Florida counties

    Options:
        - csv: whether to export results as .csv file
        - persist: whether to persist changes to DB
    """
    FloridaOwnerStateProcessor(County.BROWARD, persist, csv).process_file('NAL16F201901.csv')
    FloridaOwnerStateProcessor(County.BROWARD, persist, csv).process_file('NAP16F201901.csv')
    FloridaOwnerStateProcessor(County.MIAMIDADE, persist, csv).process_file('NAL23F201901.csv')
    FloridaOwnerStateProcessor(County.MIAMIDADE, persist, csv).process_file('NAP23F201901.csv')
    FloridaOwnerStateProcessor(County.PALMBEACH, persist, csv).process_file('NAL60F201902.csv')
    FloridaOwnerStateProcessor(County.PALMBEACH, persist, csv).process_file('NAP60F201901.csv')


@bp.cli.command('photos')
def upload_photos():
    photos_folder = photos.config.destination
    county_folders = os.listdir(photos_folder)
    for county_folder in county_folders:
        if county_folder not in County.get_counties():
            continue
        photos_files_dir = photos_folder / county_folder / 'photos'
        photos_files = os.listdir(photos_files_dir)

        # set the progress bar
        progress_bar = tqdm(total=len(photos_files))
        for photo_filename in photos_files:
            progress_bar.update(1)
            property_apn, *_ = photo_filename.split('_')

            try:
                prop = Property.query.filter_by(apn=property_apn).one()
            except NoResultFound:
                print(f'property with apn {property_apn} not found')
                continue

            prop_photo = PropertyPhoto.query.filter_by(name=photo_filename).first()

            # photo is already registered in database. Take no action just continue
            if prop_photo:
                print(f'photo is already in database {prop_photo}')
                continue
            new_photo_record = PropertyPhoto(
                property_id=prop.id,
                name=photo_filename
            )
            db.session.add(new_photo_record)
            db.session.commit()
    return


@bp.cli.command('choose_best_photo')
def choose_best_photo():
    props = db.session.query(PropertyPhoto.property_id).distinct()
    progress_bar = tqdm(total=props.count())
    for prop_id in props:
        progress_bar.update(1)
        q = PropertyPhoto.query.filter_by(property_id=prop_id)
        prop_photos = q.all()
        # filter out with no dates
        photo_dates = {prop.id:
                       extract_date_from_photo_name(prop.name)
                       for prop in prop_photos
                       if extract_date_from_photo_name(prop.name)
                       }
        # if values remain get id of max date
        if photo_dates:
            latest_date_photo_id = max(photo_dates, key=photo_dates.get)
            PropertyPhoto.query.filter_by(id=latest_date_photo_id).update(
                {'is_best': True}
            )
        # else when no values get any id
        else:
            first_photo = q.first()
            first_photo.is_best = True
        db.session.commit()
    return


@bp.cli.command('geometry')
@click.option('--persist', is_flag=True)
@click.option('--geojson', is_flag=True)
def geometry_persist(persist, geojson):
    for county in County.get_counties():
        GeometryProcessor(county=county, persist=persist, to_file=geojson).process_geometry()


@bp.cli.command('florida_obsolescence')
@click.argument('county')
@click.argument('land_use_code')
@click.option('--csv', is_flag=True)
def florida_obsolescence(county, land_use_code, csv):
    """
    Inspect presence of obsolescence records in database
    Export results in output directory
    :param county: The county
    :param csv: Whether to save to csv
    :param land_use_code: The property land use code (DOR_UC) to inspect
    """
    FloridaObsolescenceProcessor(
        provider_name=county,
        persist=False,
        to_file=csv
    ).analyze_land_use(land_use_code=int(land_use_code))


@bp.cli.command('reparse_florida_sales')
def reparse_florida_sales():
    """
    Downlaod florida sales from ftp and update database records
    """
    FLORIDA_COUNTIES = {
        16: 'broward',
        60: 'palmbeach',
        23: 'miamidade'
    }

    logger.info('Start script')

    ftp = ftplib.FTP('sdrftp03.dor.state.fl.us', 'anonymous')
    ftp.cwd('Tax Roll Data Files/2019 Final NAL - SDF Files')
    file_list = ftp.nlst()
    florida_files = [f for f in file_list if 'SDF' in f and
                     ('Broward' in f or 'Palm Beach' in f or 'Dade' in f)]

    logger.info(f'florida files found {florida_files}')

    if not florida_files:
        logger.error('no florida sale files on ftp server')
        return

    # change download directory
    new_workdir = DATA_IMPORT / 'florida_sales'
    new_workdir.mkdir(parents=True, exist_ok=True)
    os.chdir(new_workdir)
    ftp_folder = 'ftp://sdrftp03.dor.state.fl.us/Tax Roll Data Files/2019 Final NAL - SDF Files/'
    for file in florida_files:
        downloaded = wget.download(f'{ftp_folder}{file}')
        # downloaded = 'Broward 16 Final SDF 2019 sample.zip'
        if downloaded:
            logger.info(f'downloaded {os.path.abspath(downloaded)}')
            # unzip and run the parser
            with ZipFile(downloaded, 'r') as zip_ref:
                zipped = zip_ref.namelist().pop()
                extracted = zip_ref.extract(zipped)
                logger.info(f'extracted file {extracted}')
                county = FLORIDA_COUNTIES.get(int(Path(extracted).stem[3:5]))
                # run the parser
                processor = FloridaSaleProcessor(provider_name=county,
                                                 persist=True,
                                                 file_name=None,
                                                 to_file=False)
                processor.process_input_file(file_path=extracted)
        else:
            logger.error(f'could not download file {file}')


@bp.cli.command('address_unit_parser')
@click.argument('county')
def address_unit_parser(county):
    """
    Extract UNIT from address into address line2
    """
    address_parser = AddressUnitParser(county=county)
    address_parser.parse_county()


@bp.cli.command('us_address_parse')
def us_address():
    """
    Parse address field to address tokens
    """
    addr_parsed = normalize_addr_str('10276 FOX TRAIL RD S 105')
    print(addr_parsed)


@bp.cli.command('address_fix')
def address_fix():
    FixAddress().process_file(file_name='address_fix_sample.csv')


@bp.cli.command('capitalize_all_property_address_fields')
def capitalize_all_property_address_fields():
    """
    Capitalize property address fields for all counties
    """
    for county in County.get_counties():
        CapitalizeAddress().capitalize_property_addresses(county=county, persist=True, csv=True)


@bp.cli.command('capitalize_property_address_fields')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.argument('county')
def capitalize_property_address_fields(county, persist, csv):
    """
    Capitalize 'address', 'address_line_1', 'address_line_2', 'street', 'city' fields in property table
        * if length of property address field word equal to 2 then word has to stay as it is
        * if length of property address field word equal to 2 and is the last word of the field, then still capitalize
    """
    CapitalizeAddress().capitalize_property_addresses(county=county, persist=persist, csv=csv, drop_table=True)


@bp.cli.command('capitalize_all_owner_address_fields')
def capitalize_all_owner_address_fields():
    """
    Capitalize owner address fields for all counties
    """
    for county in County.get_counties():
        CapitalizeAddress().capitalize_owner_addresses(county=county, persist=True, csv=True)


@bp.cli.command('capitalize_owner_address_fields')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.argument('county')
def capitalize_owner_address_fields(county, persist, csv):
    """
    Capitalize 'address', 'address_line_1', 'address_line_2', 'street', 'city' fields in property table
        * if length of owner address field word equal to 2 then word has to stay as it is
        * if length of owner address field word equal to 2 and is the last word of the field, then still capitalize
    """
    CapitalizeAddress().capitalize_owner_addresses(county=county, persist=persist, csv=csv, drop_table=True)


@bp.cli.command('number_converter')
@click.argument('id')
@click.argument('year')
def number_converter(id, year):
    # max id in a property table
    # id = 3048144
    # year = 19

    # mask value in decimal
    mask_num = mask_to_dec()

    # create a number string
    number = int(str(id) + str(year)[-2:])

    # encode with mask to ensure that no 000001 like code will generate
    # '6BJJEJ'
    encoded = dec_to_base(number + mask_num)

    print('ID: {}'.format(id))
    print('Year: {}'.format(year))
    print("Number: {}".format(number))
    print("Encoded: {}".format(encoded))

    # decode code back to decimal
    decoded = base_to_dec(encoded)
    value = decoded - mask_num

    year = int('20{}'.format(str(value)[-2:]))
    property_id = str(value)[:-2]
    print('year: {}'.format(year))
    print('property_id: {}'.format(property_id))


@bp.cli.command('capitalize_name')
@click.argument('table_name')
def capitalize_application_names(table_name):
    from manage import app
    from app.case_management.models import Application, Client
    from sqlalchemy.exc import IntegrityError
    from app.case_management.services import CaseService

    def update_item(model, item):
        """
        Persist updated row to database
        """

        with app.app_context():
            obj = model.get(item['id'])
            try:
                if obj:
                    if item.get('first_name'):
                        obj.first_name = item.get('first_name')
                    if item.get('last_name'):
                        obj.last_name = item.get('last_name')
                    obj.save()
                    print(f'updated object with id={obj.id}')
            except IntegrityError as e:
                db.session.rollback()
                print(f'failed to update object due to {e.orig.args}')
                return e.orig.args
            return None

    import pandas as pd

    conn = create_engine(SQLALCHEMY_DATABASE_URI)
    df = pd.read_sql(
        "select id, first_name, last_name from {}".format(table_name),
        conn
    )

    if table_name == 'case_application':
        model_name = Application
    else:
        model_name = Client

    for index, row in df.iterrows():
        if row['first_name']:
            row['first_name'] = CaseService.capitalize_name_words(row['first_name'])
        if row['last_name']:
            row['last_name'] = CaseService.capitalize_name_words(row['last_name'])

        update_item(model_name, row)


@bp.cli.command('miamidade_land_type_codes')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def miamidade_land_type_codes(persist, csv):
    MiamidadeLandTypeCodeProcessor(persist, csv).process_file()


@bp.cli.command('miamidade_pool')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def miamidade_pool(persist, csv):
    MiamidadePoolProcessor(persist, csv).process_file()


@bp.cli.command('broward_pool')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def broward_pool(persist, csv):
    BrowardPoolProcessor(persist, csv).process_file()


@bp.cli.command('miamidade_insert_assessments')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
def miamidade_insert_assessments(persist, csv):
    """
    Insert data rolls for the Miamidade
    Insert owners
    """
    # insert assessment, sales
    MiamidadeRollProcessor(
        persist, csv, 'MunRoll - 00 RE - All Properties.csv', 'tent',
        db_operation=ProcessorOperation.INSERT
    ).process_file()

    # persist owners
    MiamidadePropertyOwnerProcessor(
        file_name='MunRoll - 00 RE - All Properties.csv',
        persist=persist,
        data_source='assessment',
        to_file=csv,
        created_on='2020-07-08'
    ).process_owner()


@bp.cli.command('miamidade_update_assessments')
@click.option('--persist', is_flag=True)
@click.option('--csv', is_flag=True)
@click.option('--drop_imported', is_flag=True)
def miamidade_update_assessments(persist, csv, drop_imported):
    """
    Update existed Miamidade assessments:
        - assessment_value
        - value

    Options:
        - csv: whether to export results as .csv file
        - persist: whether to persist changes to DB
        - drop_imported: whether to drop temporary imported table created
    """
    MiamidadeRollProcessor(
        persist=persist,
        csv=csv,
        file_name='MunRoll - 00 RE - All Properties.csv',
        assessment_type='tent',
        db_operation=ProcessorOperation.UPDATE,
        drop_imported=drop_imported
    ).update_assessments(assessment_date_id=10)


@bp.cli.command('miamidade_compare_assessments')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.option('--drop_imported', is_flag=True)
def miamidade_compare_assessments(persist, csv, drop_imported):
    """
    Compare two Miamidade assessments data source files

    Options:
        - csv: whether to export results as .csv file to output directory
        - persist: whether to export compare analysis to: 'assessments_changes.csv', 'cases_assessments_changes.csv'
        - drop_imported: whether to drop temporary imported table created
    """
    MiamidadeCompareAssessments(
        old_file_name='MunRoll - 00 RE - All Properties_old.csv',
        new_file_name='MunRoll - 00 RE - All Properties.csv',
        persist=persist,
        csv=csv,
        drop_imported=drop_imported
    ).compare()


@bp.cli.command('condo_codes')
@click.argument('county')
@click.option('--persist', is_flag=True)
@click.option('--csv', is_flag=True)
@click.option('--drop_imported', is_flag=True)
def condo_codes(county, persist, csv, drop_imported):
    """
    Parse condo codes for Miamidade or Broward counties

    Arguments:
        - county: choose for what county to parse, choices: 'miamidade', 'broward'

    Options:
        - csv: whether to export results as .csv file to output directory
        - persist: whether to persist results to DB
        - drop_imported: whether to drop temporary imported table created

    """
    if county == County.MIAMIDADE:
        MiamidadeCondoCodesProcessor(persist, csv, 'condoviews.csv', drop_imported=drop_imported).process_file(
            create_table=True,
            update_data=True
        )
    elif county == County.BROWARD:
        BrowardCondosProcessor(persist, csv, file_name='04 Details.xlsx', drop_imported=drop_imported).process_file()
    else:
        raise ValueError('Invalid county or county is not supported')


@bp.cli.command('miamidade_inventory_update')
@click.option('--csv', is_flag=True)
@click.option('--persist', is_flag=True)
@click.option('--drop_imported', is_flag=True)
def miamidade_inventory_update(persist, csv, drop_imported):
    """
    Update inventory fields for the Miamidade county
    Options:
        - csv: whether to export results as .csv file to output directory
        - persist: whether to persist results to DB, update 'property' table fields
        - drop_imported: whether to drop temporary table created
    """
    MiamidadeInventoryUpdateProcessor(
        persist, csv, 'MunRoll - 00 RE - All Properties.csv', drop_imported
    ).process_file()


@bp.cli.command('generate_pin_code')
def generate_pin_code():
    from manage import app
    from app.case_management.models import Application, CaseProperty
    from app.routing.services import PropertyService

    with app.app_context():
        applications = Application.query.all()
        case_properties = CaseProperty.query.all()

        for a in applications:
            if a.property_id:
                code = PropertyService.generate_code(property_id=a.property_id)
                a.pin_code = code
                a.save()

        for cp in case_properties:
            if cp.property_id:
                code = PropertyService.generate_code(property_id=cp.property_id)
                cp.pin_code = code
                cp.save()
