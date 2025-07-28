#!/usr/bin/env python
import json
from pathlib import Path

import pypdftk
from PIL import Image
import io
import os
import tempfile
import PyPDF2
import base64

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.routing.services import PropertyService
from config import APP_ROOT


def format_address(address_line):
    raw_line = address_line or ""
    formatted_address = ' '.join([w.capitalize() if w != 'FL' else w
                                  for w in raw_line.split(' ')])
    return formatted_address


def set_white_bg(png_image_encoded, png_image=None):
    """
    Since we set transparent bg for out base64 encoded signatures
    we need to set white background for proper rendering on pdf.
    Two types if input. Encoded png and pure png. If not pure png, decode png and
    proceed.
    """
    if not png_image:
        msg = base64.b64decode(png_image_encoded)
        buf = io.BytesIO(msg)
    else:  # if pure png
        buf = png_image

    im = Image.open(buf)

    fill_color = (255, 255, 255)  # your new background color

    im = im.convert("RGBA")  # it had mode P after DL it from OP
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background

    return im.convert("RGB")


def _get_tmp_filename(suffix=".pdf", delete=True):
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=delete) as fh:
        return fh.name


def sign_pdf(coords, pdf, signature, png_signature=None):
    """
    Sing pdf with signature from png
    coords: Coordinates to place signature. Format: PAGExXxYxWIDTHxHEIGHT.
      1x200x300x125x40 means page 1, 200 units horizontally from the bottom left,
      300 units vertically from the bottom left, 125 units wide, 40 units tall.
      Pages count starts at 1 (1-based indexing).  Units are pdf-standard units (1/72 inch).
    pdf: Pdf file that needs to be signed. Ex: 'foo.pdf'
    signature: base64 encoded signature from database.
    """
    page_num, x1, y1, width, height = [int(a) for a in coords.split("x")]
    page_num -= 1

    pdf_fh = open(pdf, 'rb')
    sig_tmp_fh = None

    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None

    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)

        if i == page_num:
            # Create PDF for signature
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            c.setFillColorRGB(1, 1, 0)
            c.drawImage(ImageReader(
                set_white_bg(signature,
                             png_image=png_signature)), x1, y1, width, height)
            c.showPage()
            c.save()

            # Merge PDF in to original page
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            page.mergePage(sig_page)

        writer.addPage(page)

    temp = _get_tmp_filename(delete=False)
    print(f'saving signed pdf to {temp}')

    with open(temp, 'wb') as fh:
        writer.write(fh)

    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)

    return temp


def fill_pdf(data, template='ReduxContract_digital.pdf'):
    """
    Fill pdf with data
    Template fields could be retrieved with

    from pypdftk import dump_data_fields
    dump_data_fields(pdf_template_path)

    Currently our fields are
    [{'FieldType': 'Button',
      'FieldName': 'Check Box 1',
      'FieldFlags': '0',
      'FieldValue': 'Yes',
      'FieldJustification': 'Left',
      'FieldStateOption': 'Yes'},
     {'FieldType': 'Button',
      'FieldName': 'Check Box 3',
      'FieldFlags': '0',
      'FieldValue': 'Off',
      'FieldJustification': 'Left',
      'FieldStateOption': 'Yes'},
     {'FieldType': 'Button',
      'FieldName': 'Check Box 2',
      'FieldFlags': '0',
      'FieldValue': 'Off',
      'FieldJustification': 'Left',
      'FieldStateOption': 'Yes'},
     {'FieldType': 'Button',
      'FieldName': 'Check Box 4',
      'FieldFlags': '0',
      'FieldValue': 'Off',
      'FieldJustification': 'Left',
      'FieldStateOption': 'Yes'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 2',
      'FieldFlags': '0',
      'FieldValue': 'SANTANAWILLIAM@GMAIL.COM',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 3',
      'FieldFlags': '0',
      'FieldValue': '(000) 000-0000',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 1',
      'FieldFlags': '0',
      'FieldValue': 'SANTANA WILLIAM ',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 6',
      'FieldFlags': '0',
      'FieldValue': '8585 SW 152 AVE, UNIT 234, Unincorporated County, FL 33193',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 7',
      'FieldFlags': '0',
      'FieldValue': '0000000000000',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 8',
      'FieldFlags': '0',
      'FieldValue': '2020',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 9',
      'FieldFlags': '0',
      'FieldValue': 'SANTANA WILLIAM ',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 10',
      'FieldFlags': '0',
      'FieldValue': 'SW',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 12',
      'FieldFlags': '0',
      'FieldValue': '000.000.000.000',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 15',
      'FieldFlags': '0',
      'FieldValue': '12:00:00 AM EST MM/DD/YYYYM ',
      'FieldJustification': 'Left'}]
    """
    pdf_template = Path(APP_ROOT) / 'app' / 'templates' / 'pdf' / template
    generated_pdf = pypdftk.fill_form(pdf_template, data)
    return generated_pdf
    # generated_pdf = pypdftk.fill_form(pdf_template, data, out_file='out.pdf')
    # return generated_pdf


def encode_latin1_to_utf8(file):
    with open(file, 'rb') as f:
        binary = f.read()
        binary = binary.decode('latin-1').encode('utf-8')

    return binary


def prepare_pdf_attachment(application, signature_coords):
    if application.source_id == 1:
        # means application is physical and we need to attach physical application as pdf
        data_json = json.loads(application.original_application)
        temp = _get_tmp_filename(suffix=data_json['scan_extension'], delete=False)
        with open(temp, 'wb') as f:
            pdf_binary = data_json['scan_file']
            foo = str.encode(pdf_binary).decode('utf-8').encode('latin-1')
            f.write(foo)

        return temp

    owner = ''
    if application.property and application.property.owners:
        owners_sorted_by_date = PropertyService.get_property_owners(application.property_id)
        if owners_sorted_by_date:
            latest_owner = owners_sorted_by_date[0]
            owner1 = ' '.join([latest_owner.first_name or '',
                               latest_owner.last_name or '']).strip()
            owner2 = ' '.join([latest_owner.second_owner_first_name or '',
                               latest_owner.second_owner_last_name or '']).strip()
            owner = ','.join([owner1, owner2])

    phone = application.phone_number_1 or ''

    data = {
        'Check Box 2': 'Yes' if application.application_type_id == 1 else 'Off',
        'Check Box 3': 'Yes' if application.application_type_id == 4 else 'Off',
        'Check Box 4': 'Yes' if application.application_type_id == 6 else 'Off',
        'Check Box 5': 'Yes' if application.application_type_id == 5 else 'Off',
        'Text Field 1': (application.full_name or '').upper(),
        'Text Field 2': (application.email.email_address or '').upper(),
        'Text Field 3': f'({phone[:3]}) {phone[3:6]}-{phone[6:]}' if phone else '',
        'Text Field 6': application.property.address if application.property else '',
        'Text Field 7': application.property.apn if application.property else '',
        'Text Field 8': application.tax_year or '',

        # owner field
        'Text Field 9': owner,

        'Text Field 10': application.initials or '',
        'Text Field 12': f'{application.sender_ip or ""}'.strip(),
        'Text Field 15': application.signature_updated_at.strftime(
            '%I:%M:%S %p %m/%d/%Y') if application.signature_updated_at else application.created_at.strftime(
            '%I:%M:%S %p %m/%d/%Y')
    }
    return_pdf = fill_pdf(data)
    if application.signature_base64_encoded:
        return_pdf = sign_pdf(coords=signature_coords,
                              pdf=return_pdf,
                              signature=application.signature_base64_encoded)

    return return_pdf


def invoice_pdf(application, invoice, template='ReduxInvoice.pdf'):
    """
    [{'FieldType': 'Text',
      'FieldName': 'Text Field 1',
      'FieldFlags': '0',
      'FieldValue': 'Name',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 4',
      'FieldFlags': '0',
      'FieldValue': 'Flat',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 2',
      'FieldFlags': '0',
      'FieldValue': 'Street Address',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 5',
      'FieldFlags': '0',
      'FieldValue': 'Street Address',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 3',
      'FieldFlags': '0',
      'FieldValue': 'City, ST ZIP Code',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 6',
      'FieldFlags': '0',
      'FieldValue': 'City, ST ZIP Code',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 7',
      'FieldFlags': '0',
      'FieldValue': '101',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 8',
      'FieldFlags': '0',
      'FieldValue': '9NQWJF',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 9',
      'FieldFlags': '0',
      'FieldValue': '8/7/20',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 10',
      'FieldFlags': '0',
      'FieldValue': 'Broward County Filing Fee for Folio # 514035043400',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text12',
      'FieldFlags': '0',
      'FieldValue': 'Total Due: $99,999.00',
      'FieldJustification': 'Left'},
     {'FieldType': 'Text',
      'FieldName': 'Text Field 11',
      'FieldFlags': '0',
      'FieldValue': '$99,999.00',
      'FieldJustification': 'Left'}]
  """
    prop_city = application.address_city or ""

    prop_add_1 = application.address_line1 or ''
    prop_add_2 = application.address_line2 or ''

    line_3 = f'{prop_city}' \
             f', {application.address_state} ' \
             f'{application.address_zip}'.strip().lstrip(',').strip()

    prop_address_line_1 = prop_add_1 or ''
    prop_address_line_2 = prop_add_2 if prop_add_2 else line_3
    prop_address_line_3 = line_3 if prop_add_2 else ''

    client_add_1 = invoice.client.mailing_line1 or ''
    client_add_2 = invoice.client.mailing_line2 or ''
    client_add_3 = invoice.client.mailing_line3 or ''

    county = application.property.county.capitalize()
    county = 'Miami-Dade' if county == 'Miamidade' else county

    data = {
        'Text Field 7': f'{invoice.id:06}',
        'Text Field 8': application.case_property.case_id if application.case_property else '',
        'Text Field 9': invoice.created_on.strftime('%m/%d/%y'),

        # client
        'Text Field 1': invoice.client.full_name,
        'Text Field 2': f'{client_add_1} {client_add_2}'.strip(),
        'Text Field 3': client_add_3,

        # property
        'Text Field 4': prop_address_line_1,
        'Text Field 5': prop_address_line_2,
        'Text Field 6': prop_address_line_3,

        'Text Field 10': f'{county} County '
                         f'Filing Fee for Folio # {application.property.apn}',
        'Text Field 11': '$15.00',
        'Text12': 'Total Due: $15.00',
    }

    form_filled_pdf = fill_pdf(data, template=template)
    return form_filled_pdf
