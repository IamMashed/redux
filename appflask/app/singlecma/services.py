from app.controller.properties_controller import SingleCmaController
from app.routing.services import PhotoService


class SingleCMAService:

    @classmethod
    def compute_cma_log(cls, subject, assessment, comparatives, properties_rules):
        """
        Compute Single CMA log
        """

        # create CMA controller
        cma_controller = SingleCmaController(
            subject=subject,
            subject_assessment=assessment,
            mass_cma=False,
            properties_rules=properties_rules,
            is_compute_log=True
        )

        # CMA analysis
        cma_controller.compute_cma(comps=comparatives, nearby=False)

        return cma_controller.get_formatted_cma_log()

    @classmethod
    def compute_single_cma(cls, subject, assessment, comparatives=None, nearby=None, properties_rules=None):
        """
        Compute Single CMA

        Result object:
            * subject
            * assessment
            * all comparatives
            * assessment results
            * average ranges
            * assessment results
            * assessment_date_id
        """
        # create CMA controller
        cma_controller = SingleCmaController(subject=subject, subject_assessment=assessment, mass_cma=False,
                                             properties_rules=properties_rules)

        cma_controller.compute_cma(comps=comparatives, nearby=nearby)
        # make subject photos urls
        subject = PhotoService.make_all_photos_urls(subject)

        # make comps photos urls
        all_comps = [PhotoService.make_all_photos_urls(comp) for comp in cma_controller.get_all_comps()]

        if not cma_controller.subject_property.passed_subject_sale_rule and cma_controller.mass_cma:
            # skip averages computation. use only the delta value
            avg_ranges = cma_controller.get_subject_good_sale_ranges()

        else:
            avg_ranges = cma_controller.get_all_avg_ranges()
        cma_results = {
            'subject': subject,
            'assessment': cma_controller.subject_assessment,
            'all_comps': all_comps,
            'average_ranges': avg_ranges,
            'assessment_results': cma_controller.get_derived_assessment_results(),
            'assessment_date_id': cma_controller.subject_assessment.assessment_id
        }

        return cma_results
