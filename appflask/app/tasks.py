import sys
from datetime import datetime
from tqdm import tqdm

from app import create_app, db
from app.controller.properties_controller import SingleCmaController
from app.database.models import CmaTask, CmaResult
from app.routing.services import PropertyService

app = create_app()
app.app_context().push()


def update_task_progress(job_id):
    task = CmaTask.query.get(job_id)
    if task:
        if task.complete:
            return False
        completed_amount = CmaResult.query.filter_by(task_id=job_id).count()
        progress = round(completed_amount / task.total * 100, 1)

        # calculate estimated remaining time
        current_time = datetime.now()
        remaining_time = ((current_time - task.task_ts) / completed_amount) * (task.total - completed_amount)
        remaining_time_repr = f'{remaining_time.seconds // 3600} h: {(remaining_time.seconds // 60) % 60} m'
        task.user.add_notification('task_progress', {'task_id': job_id,
                                                     'progress': f'{progress} %',
                                                     'remaining_time': remaining_time_repr})
        if progress >= 100:
            task.complete = True
            task.task_complete_ts = datetime.now()
        db.session.commit()
        return True


def mass_cma(props, job_id, sale_dates_from, sale_dates_to,
             assessment_date, assessment_ratio, rules_controller):
    pbar = tqdm(total=len(props))
    cma_results = []
    for prop in props:
        pbar.update(1)
        try:
            prop = PropertyService.get_property(property_id=prop, mass_cma=True)
            cma = SingleCmaController(prop,
                                      mass_cma=True,
                                      rules_controller=rules_controller,
                                      assessment_ratio=assessment_ratio,
                                      assessment_date=assessment_date,
                                      sale_dates_from=sale_dates_from,
                                      sale_dates_to=sale_dates_to,
                                      )
            if not cma.passed_subject_sale_rule():
                # skip averages computation. use only the delta value
                cma_result = CmaResult(task_id=job_id,
                                       property_id=prop.id,
                                       subject_sale=cma.delta,
                                       subject_sale_price=cma.subject_sale_price)
                cma_results.append(cma_result)
                continue
            cma.compute_cma()
            assmnt_values = cma.get_requested_assessment_range_values()
            total_good_comps = len(cma.get_good_comps())
            total_all_comps = len(cma.get_all_comps())
            cma_result = CmaResult(task_id=job_id,
                                   property_id=prop.id,
                                   computed_cma=assmnt_values['misc']['4'],
                                   computed_cma_medium=assmnt_values['misc']['8'],
                                   computed_cma_high=assmnt_values['misc']['12'],
                                   computed_cma_good_small=assmnt_values['good']['4'],
                                   computed_cma_good_medium=assmnt_values['good']['8'],
                                   computed_cma_good_high=assmnt_values['good']['12'],
                                   total_good_comps=total_good_comps,
                                   total_all_comps=total_all_comps,
                                   subject_sale_price=cma.subject_sale_price)
            cma_results.append(cma_result)
        except Exception as e:
            # db.session.rollback()
            app.logger.error('Unhandled exception', exc_info=sys.exc_info())
            cma_result = CmaResult(task_id=job_id,
                                   property_id=prop.id,
                                   computed_cma=None,
                                   error=repr(e))
            cma_results.append(cma_result)

    # since we are running in chunks commit at the end of chunk
    db.session.bulk_save_objects(cma_results)
    db.session.commit()
    update_task_progress(job_id)
