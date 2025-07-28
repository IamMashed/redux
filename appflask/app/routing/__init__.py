from flask import render_template
from flask_security import login_required

from app.routing.decorators import domains_allowed, Domain


class Routing:
    def init_app(self, app):
        # Routes within the app
        # @app.route('/')
        # @login_required
        # def index():
        #     return render_template('dashboard.html')

        @app.route('/')
        @app.route('/vue')
        @app.route('/vue/')
        @app.route('/vue/dashboard')
        @app.route('/vue/ratios')
        @app.route('/vue/time-adjustments')
        @app.route('/vue/cma')
        @app.route('/vue/assessment-dates')
        @app.route('/vue/rule-sets')
        @app.route('/vue/misc-settings')
        @app.route('/vue/admin')
        @app.route('/vue/lookup')
        @app.route('/vue/users/create')
        @app.route('/vue/upload-data')
        @app.route('/vue/email-templates')
        @login_required
        def vue():
            return render_template('vue/index.html')

        @app.route('/vue/applications')
        @app.route('/vue/case-management/tags')
        @login_required
        @domains_allowed(Domain.BETA, Domain.REDUX, Domain.BETA_REDUX)
        def vue_with_domains():
            return render_template('vue/index.html')

        @app.route('/vue/cma/<int:id>')
        @app.route('/vue/rule-sets/<int:id>')
        @app.route('/vue/applications/incoming/<int:id>')
        @app.route('/vue/applications/rejected/<int:id>')
        @app.route('/vue/applications/reviewed/<int:id>')
        @app.route('/vue/applications/approved/<int:id>')
        @app.route('/vue/applications/fully_rejected/<int:id>')
        @app.route('/vue/clients/<int:id>')
        @app.route('/vue/clients/<int:id>/')
        @app.route('/vue/users/<int:id>/')
        @login_required
        def vueCMA(id):
            return render_template('vue/index.html')

        @app.route('/vue/clients/<int:id>/cases/<int:child_id>')
        @login_required
        def vue_with_child(id, child_id):
            return render_template('vue/index.html')


class ApiResourceManager(object):
    """
    Api resource manager class
    """

    def __init__(self, api):
        self.api = api

    def init_resources(self):
        """
        Initialize api resources
        """
        self._add_ratios()
        self._add_adjustments()
        self._add_assessments()
        self._add_assessment_dates()
        self._add_cma()
        self._add_constants()
        self._add_counties()
        self._add_global_settings()
        self._add_nassau_villages()
        self._add_property_photos()
        self._add_property_search()
        self._add_rule_sets()
        self._add_time_adjustments()
        self._add_townships()
        self._add_case_management()
        self._add_users()
        self._add_generate_pdf()
        self._add_quick_search()
        self._add_email()
        self._add_data_mappers()

    def _add_email(self):
        from app.routing.resources import ConfirmEmailApi
        self.api.add_resource(ConfirmEmailApi, '/confirm-email/<string:token>', endpoint='confirm_email')

    def _add_quick_search(self):
        from app.search.resources import QuickSearchApi
        self.api.add_resource(QuickSearchApi, '/quick-search')

    def _add_generate_pdf(self):
        from app.pdf.resources import GeneratePdfApi
        self.api.add_resource(GeneratePdfApi, '/generate-pdf', endpoint='generate_pdf')

    def _add_users(self):
        from app.database.resources import UsersApi, UserAuthApi, UserApi, RolesApi
        self.api.add_resource(UsersApi, '/users', endpoint='users')
        self.api.add_resource(UserApi, '/users/<int:user_id>', endpoint='user')
        self.api.add_resource(UserAuthApi, '/auth', endpoint='user_auth')
        self.api.add_resource(RolesApi, '/roles', endpoint='roles')

    def _add_data_mappers(self):
        from app.database.resources import DataMappersApi, DataMapperApi, PetitionFileUploadApi
        self.api.add_resource(DataMappersApi, '/data-mappers', endpoint='data_mappers')
        self.api.add_resource(DataMapperApi, '/data-mappers/<string:name>', endpoint='data_mapper')
        self.api.add_resource(PetitionFileUploadApi, '/upload/petition')

    def _add_case_management(self):
        from app.case_management.resources import (
            ApplicationsApi, ApplicationApi, ClientsApi,
            ClientApi, CasePropertiesApi, CasePropertyApi, NoteApi,
            TagsApi, TagApi, ApplicationTypesApi, ApplicationDuplicationsApi,
            ApplicationNotesApi, ClientNotesApi,
            ApplicationStatusesApi, PaymentTypesApi, LookupApi, ClientTypesApi,
            CasePropertyNotesApi, MarketingCodeApi, PropertyHistoryApi,
            ApplicationRejectApi, ApplicationApproveApi,
            RejectReasonsApi, CaseInfoApi, ApplicationFullyRejectApi,
            PhysicalApplicationsApi, TakeoversApi,
            TakeoverApi, ApplicationSourcesApi, PaymentStatusesApi,
            ApplicationReviewApi, ApplicationRepairApi,
            ApplicationAttachmentApi, ApplicationSignEmailApi, CaseReportApi,
            CaseListApi, CaseExtendedListApi, CasePropertiesDr486Api, CasePropertyEvidencePackageApi,
            CasePropertyWorkupsApi, WorkupEvidencePackageApi, CasePetitionsReportApi, LookupReportApi,
            SendEmailApi
        )

        # Takeover
        self.api.add_resource(
            TakeoversApi,
            '/takeovers',
            '/applications/<int:application_id>/takeovers',
            endpoint='case_takeovers'
        )
        self.api.add_resource(TakeoverApi, '/takeovers/<int:takeover_id>', endpoint='case_takeover')

        # Client types
        self.api.add_resource(ClientTypesApi, '/client-types', endpoint='client_types')

        # Application sources
        self.api.add_resource(ApplicationSourcesApi, '/application-sources', endpoint='application_sources')

        # Client lookup
        self.api.add_resource(LookupApi, '/lookup/<string:entity_name>', endpoint='lookup')
        self.api.add_resource(LookupReportApi, '/lookup/<string:entity_name>/lookup-results')
        self.api.add_resource(CaseReportApi, '/lookup/<string:entity_name>/report', endpoint='lookup_case_report')
        self.api.add_resource(CaseExtendedListApi,
                              '/lookup/<string:entity_name>/case_extended_list',
                              endpoint='lookup_case_extended_list')
        self.api.add_resource(CaseListApi,
                              '/lookup/<string:entity_name>/case_list',
                              endpoint='lookup_case_list')

        # Petitions report
        self.api.add_resource(CasePetitionsReportApi, '/lookup/<string:entity_name>/petitions-report')

        # Application statuses
        self.api.add_resource(ApplicationStatusesApi, '/application-statuses', endpoint='application_statuses')

        # Payment types
        self.api.add_resource(PaymentTypesApi, '/payment-types', endpoint='payment_types')

        # Payment statuses
        self.api.add_resource(PaymentStatusesApi, '/payment-statuses', endpoint='payment_statuses')

        # Case Info
        self.api.add_resource(CaseInfoApi, '/case-info', endpoint='case_info')

        # Case Tags
        self.api.add_resource(TagsApi, '/tags', endpoint='case_tags')

        # Case Tag
        self.api.add_resource(TagApi, '/tags/<int:tag_id>', endpoint='case_tag')

        # Case Applications
        self.api.add_resource(ApplicationsApi, '/applications', endpoint='case_applications')

        # Physical Application
        self.api.add_resource(PhysicalApplicationsApi, '/applications/physical', endpoint='physical_application')

        # Case Application
        self.api.add_resource(ApplicationApi, '/applications/<int:application_id>', endpoint='case_application')

        # Case Clients
        self.api.add_resource(ClientsApi, '/clients', endpoint='case_clients')

        # Case Client
        self.api.add_resource(ClientApi, '/clients/<int:client_id>', endpoint='case_client')

        # Case Properties
        self.api.add_resource(CasePropertiesApi, '/case-properties', '/clients/<int:client_id>/case-properties',
                              endpoint='case_properties')

        self.api.add_resource(CasePropertiesDr486Api, '/case-properties/<int:case_id>/dr486',
                              endpoint='case_properties_dr486')

        # Case evidence package
        self.api.add_resource(
            CasePropertyEvidencePackageApi,
            '/case-properties/<int:case_property_id>/evidence-package',
            endpoint='case_properties_evidence_package'
        )

        self.api.add_resource(WorkupEvidencePackageApi, '/single-cma-workups/<int:workup_id>/evidence-package',
                              endpoint='workup_evidence_package')

        # Case workups
        self.api.add_resource(CasePropertyWorkupsApi, '/case-properties/<int:case_property_id>/single-cma-workups',
                              endpoint='case_property_single_cma_workups')

        # Case Property
        self.api.add_resource(CasePropertyApi, '/case-properties/<int:case_property_id>', endpoint='case_property')

        # Case Notes
        self.api.add_resource(ApplicationNotesApi, '/applications/<int:application_id>/notes',
                              endpoint='application_notes')
        self.api.add_resource(ClientNotesApi, '/clients/<int:client_id>/notes', endpoint='client_notes')
        self.api.add_resource(CasePropertyNotesApi, '/case-properties/<int:case_property_id>/notes',
                              endpoint='case_property_notes')
        self.api.add_resource(NoteApi, '/notes/<int:note_id>', endpoint='case_note')

        # Application types
        self.api.add_resource(ApplicationTypesApi, '/application-types', endpoint='case_application_types')

        # Marketing codes
        self.api.add_resource(MarketingCodeApi, '/marketing-codes', endpoint='case_marketing_codes')

        # Application duplicates
        self.api.add_resource(ApplicationDuplicationsApi, '/applications/<int:application_id>/duplications',
                              endpoint='case_application_duplicates')

        # Application property history
        self.api.add_resource(PropertyHistoryApi, '/applications/<int:application_id>/history')

        # Application reject
        self.api.add_resource(ApplicationRejectApi, '/applications/<int:application_id>/reject',
                              endpoint="reject_application")

        # Application fully reject
        self.api.add_resource(ApplicationFullyRejectApi, '/applications/<int:application_id>/fully-reject',
                              endpoint="fully_reject_application")

        # Application review
        self.api.add_resource(ApplicationReviewApi, '/applications/<int:application_id>/review',
                              endpoint="review_application")

        # Application approve
        self.api.add_resource(ApplicationApproveApi, '/applications/<int:application_id>/approve',
                              endpoint="approve_application")

        # Reject reasons
        self.api.add_resource(RejectReasonsApi, '/reject-reasons', endpoint='reject_reasons')

        # Repair application
        self.api.add_resource(ApplicationRepairApi, '/applications/<int:application_id>/repair',
                              endpoint="repair_application")

        # Application scan
        self.api.add_resource(ApplicationAttachmentApi, '/applications/<int:application_id>/attachment',
                              endpoint="application_attachment")

        # Application sing email
        self.api.add_resource(ApplicationSignEmailApi, '/applications/<int:application_id>/sign-email',
                              endpoint="application_sign_email")

        self.api.add_resource(SendEmailApi, '/send-email', endpoint='send_email')

    def _add_ratios(self):
        # Ratios
        from app.settings.resources import RatiosSettingsResource, RatioResource, RatiosResource

        self.api.add_resource(RatiosSettingsResource, '/ratiossets')
        self.api.add_resource(RatioResource, '/ratiossets/ratios/<id>')
        self.api.add_resource(RatiosResource, '/ratiossets/ratios')

    def _add_time_adjustments(self):
        from app.settings.resources import TimeAdjustmentsApi, TimeAdjustmentApi

        self.api.add_resource(TimeAdjustmentsApi, '/settings/time-adjustments')
        self.api.add_resource(TimeAdjustmentApi, '/settings/time-adjustments/<int:adjmnt_id>')

    def _add_assessments(self):
        from app.database.resources import AssessmentApi, AssessmentsApi
        self.api.add_resource(AssessmentApi, '/assessments/<int:assessment_id>')
        self.api.add_resource(AssessmentsApi, '/settings/assessment-dates/<int:assessment_date_id>/assessments')

    def _add_assessment_dates(self):
        from app.settings.resources import AssessmentDatesApi, AssessmentDateApi

        self.api.add_resource(AssessmentDatesApi, '/settings/assessment-dates')
        self.api.add_resource(AssessmentDateApi, '/settings/assessment-dates/<int:assmnt_id>')

    def _add_global_settings(self):
        from app.settings.resources import GlobalSettingsApi, GlobalSettingApi

        self.api.add_resource(GlobalSettingsApi, '/global-settings', endpoint="global_settings")
        self.api.add_resource(GlobalSettingApi, '/global-settings/<int:setting_id>', endpoint="global_setting")

    def _add_property_search(self):
        from app.database.resources import PropertiesApi, PropertyApi

        self.api.add_resource(PropertiesApi, '/properties', endpoint='properties')
        self.api.add_resource(PropertyApi, '/properties/<int:property_id>', endpoint='property')

    def _add_property_photos(self):
        from app.rules.resources import PhotosApi, PhotoApi

        self.api.add_resource(
            PhotosApi,
            '/properties/<int:property_id>/photos',
            '/properties/best-photos',
            endpoint='property_photos'
        )
        self.api.add_resource(
            PhotoApi,
            '/properties/<int:property_id>/best-photo',
            '/properties/<int:property_id>/photos/<int:photo_id>',
            endpoint='property_photo'
        )

    def _add_counties(self):
        from app.database.resources import CountiesApi
        self.api.add_resource(CountiesApi, '/counties', endpoint='counties')

    def _add_townships(self):
        from app.database.resources import TownshipsApi
        self.api.add_resource(TownshipsApi, '/counties/<string:county_name>/townships', endpoint='townships')

    def _add_nassau_villages(self):
        from app.database.resources import VillagesApi
        self.api.add_resource(VillagesApi, '/counties/<string:county_name>/villages', endpoint='villages')

    def _add_rule_sets(self):
        # Rule sets
        from app.rules.resources import RuleSetsApi, RuleSetApi, SelectionRulesApi, SelectionRuleApi, \
            InventoryRulesApi, InventoryRuleApi, ObsolescenceApi

        self.api.add_resource(
            RuleSetsApi,
            '/rule-sets',
            '/settings/assessment-dates/<int:assessment_date_id>/rule-sets',
            endpoint='rule_sets'
        )

        self.api.add_resource(RuleSetApi, '/rule-sets/<int:rule_set_id>', endpoint='rule_set')

        # Selection rules
        self.api.add_resource(
            SelectionRulesApi,
            '/selection-rules',
            '/rule-sets/<int:rule_set_id>/selection-rules',
            endpoint='selection_rules'
        )
        self.api.add_resource(SelectionRuleApi, '/selection-rules/<int:rule_id>', endpoint='selection_rule')

        # Inventory rules
        self.api.add_resource(
            InventoryRulesApi,
            '/inventory-rules',
            '/rule-sets/<int:rule_set_id>/inventory-rules',
            endpoint='inventory_rules'
        )
        self.api.add_resource(InventoryRuleApi, '/inventory-rules/<int:rule_id>', endpoint='inventory_rule')

        # Obsolescence rules
        self.api.add_resource(ObsolescenceApi, '/obsolescence-rules', endpoint='obsolescence_rules')

    def _add_adjustments(self):
        # Adjustments
        from app.rules.resources import AdjustmentsApi
        self.api.add_resource(AdjustmentsApi, '/adjustments', endpoint='adjustments')

    def _add_cma(self):
        # Single CMA
        from app.singlecma.resources import SingleCMAApi, SingleCMAPropertyApi, SingleCMALogApi
        from app.singlecma.resources import SingleCMAWorkupApi, SingleCMAWorkupsApi, FileApi

        self.api.add_resource(SingleCMALogApi, '/single-cma/log', endpoint='single_cma_log')
        self.api.add_resource(SingleCMAApi, '/single-cma', '/single-cma/<int:property_id>', endpoint='single_cma')
        self.api.add_resource(SingleCMAPropertyApi, '/properties/<int:property_id>/single-cma')

        self.api.add_resource(SingleCMAWorkupsApi, '/single-cma-workups', endpoint='single_cma_workups')
        self.api.add_resource(SingleCMAWorkupApi, '/single-cma-workups/<int:workup_id>', endpoint='single_cma_workup')
        self.api.add_resource(FileApi, '/files/<int:file_id>', endpoint='file')

    def _add_constants(self):
        # Constants
        from app.routing.resources import ConstantsApi
        self.api.add_resource(ConstantsApi, '/constants', endpoint='constants')
