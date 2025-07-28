from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import click

from app.database.models import Assessment
from app.database.models.property import Property

import pandas as pd

from config import DATA_IMPORT, MAX_WORKER_COUNT

pd.options.mode.chained_assignment = None  # default='warn'


class Processor(object):

    def __init__(self, folder_name, app,
                 persist=False, csv_output=False):
        self.folder_name = folder_name
        self.persist = persist
        self.csv_output = csv_output
        self.app = app

    def commit_row(self, row):
        with self.app.app_context():
            errors = dict()
            prop = Property.query.filter_by(apn=row.par_id).first()
            if not prop:
                errors['property'] = f'property with apn {row.par_id} not in database'
            else:
                # update property with data coming from assessment
                prop.school_district = row.sch_code
                prop.property_class = row.prop_class
                # db.session.flush()

                error_at_db = Assessment.insert(
                    dict(
                        value=row.total_av,
                        assessment_value=row.total_av,
                        # assessment_date=f'01-01-{row.roll_yr}',
                        assessment_type='final',
                        property_id=prop.id,
                        assessment_id=11
                    )
                )
                if error_at_db:
                    print(error_at_db)
                    errors['database_operation'] = error_at_db

            # if errors:
            #     AssessmentValidation.insert(
            #         row.par_id, 'suffolk', errors)

    def store_as_csv(self, df):
        output_folder = DATA_IMPORT / 'output' / self.folder_name / 'assessment'
        output_folder.mkdir(parents=True, exist_ok=True)
        output_path = output_folder / f'{self.folder_name}.csv'
        df.to_csv(output_path, index=None)

    def join_dataframes(self):
        """Join all the property sources into one dataframe"""
        first = DATA_IMPORT / 'src' / self.folder_name / 'assessment' / 'assessment.txt'
        first_df = pd.read_csv(first,
                               usecols=['muni_code',
                                        'parcel_id',
                                        'roll_yr',
                                        'prop_class',
                                        'total_av',
                                        'sch_code'],
                               sep='\t',
                               dtype='str')

        second = DATA_IMPORT / 'src' / 'suffolk' / 'property' / 'parcel_parid.txt'
        second_df = pd.read_csv(second,
                                usecols=['par_id',
                                         'parcel_id',
                                         'muni_code'],
                                dtype='str')
        df = pd.merge(first_df, second_df, how='left',
                      on=['muni_code', 'parcel_id'])

        return df

    def process_input_file(self):
        joined_df = self.join_dataframes()
        joined_df = joined_df.replace({pd.np.nan: ''})
        print('joined frames...')

        if self.persist:
            with ThreadPoolExecutor(MAX_WORKER_COUNT) as executor:
                futures = []
                with click.progressbar(
                        length=joined_df.shape[0],
                        label='suffolk step 1 / 2...') as bar:
                    for row in joined_df.itertuples():
                        bar.update(1)
                        futures.append(
                            executor.submit(self.commit_row, row))
                with click.progressbar(
                        length=joined_df.shape[0],
                        label='suffolk step 2 / 2...') as bar:
                    for _ in as_completed(futures):
                        bar.update(1)

        if self.csv_output:
            joined_df['assessment_id'] = 11
            joined_df['assessment_type'] = Assessment.FINAL
            self.store_as_csv(joined_df)

        return None
