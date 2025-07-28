import base64

from flask import request
from flask_restful import Resource
from flask_weasyprint import render_pdf

from app.case_management.models import ApplicationType, MarketingCode, Client
from app.pdf.generate_pdf import QrCodeGenerator, PdfGenerator
from app.utils.constants import County


class GeneratePdfApi(Resource):

    @classmethod
    def valid_client_id(cls, client_id):
        if client_id and Client.get(client_id):
            return True
        return False

    @classmethod
    def valid_year(self, year):
        if year and 1900 <= year <= 2050:
            return True
        return False

    @classmethod
    def get_marketing_code_id(cls, marketing_code):
        if marketing_code:
            code = MarketingCode.get_by(name=marketing_code)
            if code:
                return code.id
        return MarketingCode.get_default()

    @classmethod
    def get_application_type_id(cls, application_type):
        if application_type:
            app_type = ApplicationType.get_by(name=application_type)
            if app_type:
                return app_type.id

        return ApplicationType.get_default()

    @classmethod
    def get_context(cls, data):
        # read get parameters
        apn = data.get('apn', None, str)
        tax_year = data.get('tax_year', None, int)
        application_type = data.get('application_type', None, str)
        county_name = data.get('county', None, str)
        marketing_code = data.get('marketing_code', None, str)
        client_id = data.get('client_id', None, int)

        marketing_code_id = GeneratePdfApi.get_marketing_code_id(marketing_code)
        application_type_id = GeneratePdfApi.get_application_type_id(application_type)
        county = County.get_code(county_name)

        if not GeneratePdfApi.valid_client_id(client_id):
            client_id = None

        if not GeneratePdfApi.valid_year(tax_year):
            tax_year = None

        qr_code = QrCodeGenerator()
        qr_code.generate(
            apn=apn,
            tax_year=tax_year,
            application_type_id=application_type_id,
            county=county,
            marketing_code_id=marketing_code_id,
            client_id=client_id
        )
        encoded = base64.b64encode(qr_code.stream.getvalue()).decode("ascii")
        context = {
            'apn': apn or '',
            'county': county_name if county else '',
            'tax_year': tax_year or '',
            'application_type': ApplicationType.get(application_type_id).name,
            'marketing_code': MarketingCode.get(marketing_code_id).name,
            'client_id': client_id or '',
            'qr_code': encoded
        }
        return context

    def get(self):

        context = self.get_context(request.args)
        pdf = PdfGenerator.from_template('pdf/pdf_template.html', context)
        response = render_pdf(pdf)

        response.headers['Content-Type'] = "application/pdf"
        # response.headers['Content-Disposition'] = 'attachment; application.pdf'
        response.headers['Content-Disposition'] = 'inline; filename=application.pdf'

        return response
