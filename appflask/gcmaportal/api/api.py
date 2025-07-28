from app.routing import ApiResourceManager


class PublicApiResourceManager(ApiResourceManager):
    """
    Public API resource manager class
    """

    def init_resources(self):
        self._add_status()
        self._add_property()
        self._add_properties()
        self._add_applications()
        self._generate_pdf()

    def _generate_pdf(self):
        from gcmaportal.api.resources import PublicPdfApi
        self.api.add_resource(PublicPdfApi, '/generate-pdf', endpoint='public_pdf')

    def _add_status(self):
        from gcmaportal.api.resources import StatusApi
        self.api.add_resource(StatusApi, '/status', endpoint='api_status')

    def _add_property(self):
        from gcmaportal.api.resources import PublicPropertyApi
        self.api.add_resource(PublicPropertyApi, '/property', endpoint='public_property')

    def _add_properties(self):
        from gcmaportal.api.resources import PublicPropertiesApi
        self.api.add_resource(PublicPropertiesApi, '/properties', endpoint='public_properties')

    def _add_applications(self):
        from gcmaportal.api.resources import DigitalApplicationsApi, DigitalApplicationApi
        self.api.add_resource(DigitalApplicationsApi, '/applications', endpoint='public_applications')
        self.api.add_resource(DigitalApplicationApi, '/applications/<string:token>', endpoint='public_application')
