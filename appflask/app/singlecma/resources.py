import json
import logging
import sys
from datetime import datetime

from flask import request, current_app, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app import db
from app.case_management.models import CaseProperty, Note, NoteSender, NoteDescription, NoteType
from app.controller.properties_controller import SingleCmaController
from app.database.models import Files
from app.database.models.user import Permission
from app.routing.decorators import permission_required, prop_id_allowed, gzipped
from app.routing.errors import not_found, bad_request, server_error
from app.routing.services import PropertyService
from app.rules import exceptions
from app.rules.exceptions import AssessmentException, SubjectLacksDataException, NotEnoughCompsException
from app.singlecma.models import SingleCMASchema, SingleCMAWorkupsSchema, SingleCMAWorkups
from app.singlecma.services import SingleCMAService
from app.utils.functions import jsonify  # Faster


# from app.utils.constants import timeit


class SingleCMAPropertyApi(Resource):
    def post(self, property_id):
        # deserialize json data single cma objects
        json_data = request.get_json()
        json_data['all_comps'][0]['id'] = property_id

        cma_objects = SingleCMASchema().load(json_data)

        # get subject from the request
        subject = cma_objects.get('subject')

        # get all comparatives from the request
        comparative = cma_objects.get('all_comps')[0]

        # get properties rules
        properties_rules = cma_objects.get('rule_set')

        # the property assessment
        assessment = cma_objects.get('assessment', None) or PropertyService.get_property_assessment(subject.id)

        # create CMA controller
        cma_controller = SingleCmaController(
            subject=subject,
            subject_assessment=assessment,
            mass_cma=False,
            properties_rules=properties_rules,
        )

        # just analyze single comparative
        analyzed_comp = cma_controller.analyse_comp(comparative)

        cma_results = {
            'subject': subject,
            'all_comps': [analyzed_comp],
        }
        return jsonify(SingleCMASchema().dump(cma_results))


class SingleCMALogApi(Resource):
    def post(self):
        """
        Get property Single CMA log
        """
        try:
            # deserialize json data single cma objects
            json_data = request.get_json()
            cma_objects = SingleCMASchema().load(json_data)

            # get subject from the request
            subject = cma_objects.get('subject')

            # get all comparatives from the request
            all_comps = cma_objects.get('all_comps', None)

            # get properties rules
            rule_set = cma_objects.get('rule_set', None)

            # get assessment
            assessment = cma_objects.get('assessment', None)

            cma_log = SingleCMAService.compute_cma_log(
                subject=subject,
                assessment=assessment,
                comparatives=all_comps,
                properties_rules=rule_set
            )

            return jsonify(cma_log)
        except Exception as e:
            import traceback
            logging.error(traceback.print_exc(file=sys.stdout))
            traceback.print_exc(file=sys.stdout)
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class SingleCMAApi(Resource):

    @permission_required(Permission.SINGLE_CMA)
    @prop_id_allowed
    @gzipped
    def get(self, property_id):
        """
        Get Single CMA computation
        :param property_id: The id of subject property
        """
        # get the subject property
        subject = PropertyService.get_property(property_id)

        if subject is None:
            return not_found("Property with id {} was not found".format(property_id))

        # get nearby attribute from the request
        nearby = request.args.get('nearby', default=None, type=bool)

        # get assessment date id
        assessment_date_id = request.args.get('assessment_date_id', type=int)

        try:
            # the property assessment
            assessment = PropertyService.get_property_assessment(subject.id, assessment_date_id=assessment_date_id)

            if not assessment:
                raise exceptions.AssessmentException('No subject assessment')

            if subject.geo is None:
                raise exceptions.SubjectLacksDataException('No subject geo')

            # compute single cma
            cma_results = SingleCMAService.compute_single_cma(subject=subject, assessment=assessment, nearby=nearby)
            return jsonify(SingleCMASchema().dump(cma_results))
        except NotEnoughCompsException as e:
            return server_error(message=e.args[0])
        except SubjectLacksDataException as e:
            return server_error(message=e.args[0])
        except AssessmentException as e:
            return server_error(message=e.args[0])
        except Exception as e:
            import traceback
            traceback.print_exc(file=sys.stdout)
            if current_app.debug:
                current_app.logger.debug(traceback.print_exc(sys.stdout))
            response = jsonify(e.args)
            response.status_code = 500
            return response

    # @timeit
    @permission_required(Permission.SINGLE_CMA)
    def post(self):
        """
        Re-compute CMA for requested subject & comparatives
        """

        # deserialize json data single cma objects
        json_data = request.get_json()
        cma_objects = SingleCMASchema().load(json_data)

        try:
            # re-compute CMA
            cma_results = SingleCMAService.compute_single_cma(
                subject=cma_objects.get('subject'),
                assessment=cma_objects.get('assessment', None),
                comparatives=cma_objects.get('all_comps', None),
                properties_rules=cma_objects.get('rule_set', None)
            )

            return jsonify(SingleCMASchema().dump(cma_results))
        except NotEnoughCompsException as e:
            return server_error(message=e.args[0])
        except SubjectLacksDataException as e:
            return server_error(message=e.args[0])
        except AssessmentException as e:
            return server_error(message=e.args[0])
        except Exception as e:
            response = jsonify(error=e.args)
            response.status_code = 500
            return response


class SingleCMAWorkupsApi(Resource):

    def post(self):
        """
        Add new single cma workup
        """
        data = request.form.get("data")
        report_file = request.files.get('report_file')
        good_bad_report_file = request.files.get('good_bad_report_file')

        try:
            json_data = json.loads(data)
            property_id = json_data.get('property_id')
            is_primary = json_data.get('is_primary')

            case_property = CaseProperty.get_by(property_id=property_id)
            if not case_property:
                return bad_request(f"Can not create workup. No case for the property with id={property_id}")

            new_file = Files.create_from_file(report_file)
            report_file_id = new_file.id
            good_bad_report_file_id = None

            if good_bad_report_file:
                new_file = Files.create_from_file(good_bad_report_file)
                good_bad_report_file_id = new_file.id

            if is_primary:
                # update is_primary=False for all property workups
                db.session.query(SingleCMAWorkups).filter(
                    SingleCMAWorkups.case_property_id == case_property.id
                ).update({'is_primary': False})
                db.session.commit()
            elif db.session.query(SingleCMAWorkups).filter(
                    SingleCMAWorkups.case_property_id == case_property.id).count() == 0:
                is_primary = True

            # prepare workup data
            json_data['report_file_id'] = report_file_id
            json_data['good_bad_report_file_id'] = good_bad_report_file_id
            json_data['created_at'] = str(datetime.now())
            json_data['is_primary'] = is_primary
            json_data['case_property_id'] = case_property.id

            new_workup = SingleCMAWorkupsSchema().load(json_data)
            new_workup.save()

            # log workup created case activity
            Note.create_system_note(
                note_sender=NoteSender.CASE_PROPERTY,
                obj=case_property,
                note_text=NoteDescription.WORKUP_CREATED,
                note_type=NoteType.WORKUP_CREATED
            )

            return jsonify(SingleCMAWorkupsSchema(exclude=('cma_payload', )).dump(new_workup))

        except IntegrityError:
            db.session.rollback()
            import traceback
            return server_error(message=traceback.format_exc())
        except Exception:
            import traceback
            return server_error(traceback.format_exc())


class SingleCMAWorkupApi(Resource):
    def get(self, workup_id):
        """
        Get specific single cma workup
        """
        try:
            workup = SingleCMAWorkups.get_or_404(workup_id)
            return jsonify(SingleCMAWorkupsSchema().dump(workup))
        except HTTPException:
            return not_found(message=f"Single CMA workup with id={workup_id} was not found")

    def put(self, workup_id):
        """
        Update specific single cma workup

        Allowed to update:
        - is_primary: True/False
        """
        try:
            json_data = request.get_json()
            json_data['id'] = workup_id

            updated_workup = SingleCMAWorkupsSchema(only=('id', 'is_primary',)).load(json_data)
            updated_workup.save()
            logging.info(f"Workup with id={workup_id} was updated at {datetime.now()}")

            return jsonify(SingleCMAWorkupsSchema().dump(updated_workup))
        except Exception as e:
            db.session.rollback()
            return server_error(e.args[0])

    def delete(self, workup_id):
        """
        Delete specific single cma workup
        """
        try:
            workup = SingleCMAWorkups.get_or_404(workup_id)
            workup.delete()
            logging.info(f"Workup with id={workup_id} was deleted at {datetime.now()}")

            return jsonify({'status': True})
        except HTTPException:
            return not_found(message=f"Single CMA workup with id={workup_id} was not found")


class FileApi(Resource):
    def get(self, file_id):
        file = Files.get(file_id)

        response = make_response(file.data)
        response.headers['Content-Type'] = "application/pdf"
        response.headers['Content-Disposition'] = f'inline; filename={file.name}'

        return response
