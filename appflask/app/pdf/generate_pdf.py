import base64

from config import IMAGES_OBSERVER_DIR
from my_logger import logger
import io
import tempfile

import pyqrcode
from PIL import Image
from flask import render_template
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from weasyprint import HTML

from app.utils.constants import County


class QrCodeGenerator:
    """
    - Property APN Number
    - Tax Year
    - Application Type
    - County
    - Marketing Code (not required)
    - Prospect / Client ID (not required)
    """

    def __init__(self):
        self.code = None
        self.data = None
        self.stream = None

    def generate_from_application(self, apn, tax_year, application_type, county,
                                  marketing_code=None, client_id=None):
        self.generate(
            apn=apn,
            tax_year=tax_year,
            application_type=application_type,
            county=county,
            marketing_code=marketing_code,
            client_id=client_id
        )

    def make_data(self, **kwargs):
        data = ''
        for kw in kwargs:
            if kwargs[kw]:
                data = data + '{}={}&'.format(str(kw), kwargs[kw])
        data = data[:-1]

        return data

    @staticmethod
    def parse_qr_code_data(qr_code_data):
        """
        Parse pdf data
        """
        dict_data = {}
        if qr_code_data:
            try:
                splits = [s.strip() for s in qr_code_data.split(',')]
                dict_data['apn'] = splits[0]
                dict_data['county'] = County.get_code(splits[1])
                dict_data['tax_year'] = int(splits[2])
                dict_data['application_type'] = splits[3].lower()
                dict_data['marketing_code_id'] = int(splits[4])
            except Exception as e:
                logger.error("Invalid qr code data format")
                logger.error(e)
                return {}
        return dict_data

    def generate(self, **kwargs):
        """
        Generate QR code
        """

        self.data = self.make_data(**kwargs)
        self.code = pyqrcode.create(content=self.data)
        stream = io.BytesIO()

        self.code.png(stream, scale=6)
        self.stream = stream
        return self

    def decode_scan(self, scan_path):
        """
        Decode scan contain QR code
        """
        image = Image.open(scan_path)
        qr_code_data = None
        for qr_code in decode(image):
            qr_code_data = qr_code.data.decode("utf-8")

        # buffered = io.BytesIO()
        # image.save(buffered, 'png')
        # image_bytes = buffered.getvalue()

        parsed_data = self.parse_qr_code_data(qr_code_data)

        # return parsed_data, image_bytes
        return parsed_data

    def get_base64_encoded(self, file_path):
        with open(file_path, "rb") as img_file:
            base64_encoded = base64.b64encode(img_file.read())
        return base64_encoded

    def decode_file(self, file_path):
        logger.info("Start 'decode_file'")
        try:
            with tempfile.TemporaryDirectory(dir=IMAGES_OBSERVER_DIR) as path:
                paths = convert_from_path(file_path, fmt='png', paths_only=True, output_folder=path)
                logger.info('output folder: ' + paths[0])

                data = self.decode_scan(paths[0])
                ext = '.pdf'

                logger.info(f'Parsed data: {data}')
                logger.info(f'Extension: {ext}')

                with open(file_path, 'rb') as binary_file:
                    binary_file_data = binary_file.read()
                    decoded = binary_file_data.decode('latin-1')

                encoded = decoded.encode('utf-8')
                base64_encoded = self.get_base64_encoded(paths[0])

                return data, encoded, ext, base64_encoded
        except Exception as e:
            logger.error(e)

    def save(self, file_name):
        if self.code:
            self.code.png(file_name)


class PdfGenerator:

    @classmethod
    def from_template(cls, template, context, write_pdf=False):
        html_string = render_template(template, **context)

        if write_pdf:
            HTML(string=html_string).write_pdf('output.pdf')
        return HTML(string=html_string)


if __name__ == '__main__':
    print(QrCodeGenerator().decode_scan('scan_sample.png'))
