from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import click
import pdftotext
import pandas as pd

from app import db
from app.database.models import Property, Assessment
from app.database.models.assessment import AssessmentValidation
from config import DATA_IMPORT


class BabylonAssessmentProcessor:

    def __init__(self, file_name, to_csv=False, persist=False):
        self.file_name = file_name
        self.to_csv = to_csv
        self.persist = persist
        self.properties = Property.query.with_entities(
            Property.id, Property.apn, Property.county
        ) if self.persist else None

    @staticmethod
    def format_parcel(parcel):
        splitted = [d for d in parcel.split(' ') if d]
        return ''.join([splitted[0],
                        splitted[1].zfill(6),
                        splitted[2].zfill(5),
                        splitted[3].zfill(7)]).replace('.', '')

    @staticmethod
    def get_parcel_and_assessment(records):
        result = []
        for record in records:
            lines = record.splitlines()
            assessed = lines[4].split('!')[-2].strip()
            parcel = BabylonAssessmentProcessor.format_parcel(
                lines[-1].split('!')[1].strip())
            result.append(dict(
                parcel=parcel,
                assessed=assessed
            ))
        return pd.DataFrame(result)

    def commit_assessments(self, df):
        errors = dict()
        for item in df.itertuples():
            prop = self.properties.filter_by(apn=item.parcel,
                                             county='suffolk').first()
            if not prop:
                errors['property'] = f'property with apn {item.parcel} not in database'
            else:
                error_at_db = Assessment.insert(
                    dict(value=item.assessed,
                         # assessment_date=item.assessment_date,
                         assessment_type=item.assessment_type,
                         property_id=prop.id
                         ))
                if error_at_db:
                    errors['database_operation'] = error_at_db

            if errors and not df.empty:
                AssessmentValidation.insert(
                    item.parcel, 'suffolk', errors)

        db.session.commit()

    def process_page(self, raw_page):
        records = raw_page.split(
            '!---------------------------------------------------------------------------------------!\n')

        # rest of the records
        result_df = BabylonAssessmentProcessor.get_parcel_and_assessment(
            records[2:-2])
        # used to extract date and type
        header = records[0]
        # year = header.split('YEAR ')[1][:4]
        date_and_type = header.split('VALUATION DATE - ')[1]. \
            strip().split(' ')

        # result_df['assessment_date'] = ' '.join([
        #     date_and_type[1],
        #     date_and_type[0],
        #     year
        # ])
        result_df['assessment_type'] = date_and_type[-1]
        if self.persist:
            from manage import app
            with app.app_context():
                self.commit_assessments(result_df)
        return result_df

    def store_as_csv(self, df):
        output_folder = DATA_IMPORT / 'output' / 'suffolk' / 'babylon'
        output_folder.mkdir(parents=True, exist_ok=True)
        output_path = output_folder / f'{self.file_name}.csv'
        df.to_csv(output_path, index=None)

    def process_babylon_pdf(self):
        target_path = DATA_IMPORT / 'src' / 'suffolk' / 'babylon' / f'{self.file_name}.pdf'

        with open(target_path, 'rb') as f:
            pdf = pdftotext.PDF(f)
        output_df = pd.DataFrame()

        with ThreadPoolExecutor() as executor:
            futures = []
            with click.progressbar(pdf, label='babylon step 1 / 2') as bar:
                for foo in bar:
                    futures.append(executor.submit(
                        self.process_page, foo))
            print('submitted to executor')
            with click.progressbar(length=len(pdf),
                                   label='babylon step 2 / 2') as bar:
                for future in as_completed(futures):
                    bar.update(1)
                    if self.to_csv:
                        output_df = output_df.append(future.result(),
                                                     ignore_index=True,
                                                     sort=False)
        if self.to_csv:
            self.store_as_csv(output_df)


if __name__ == '__main__':
    from manage import app
    with app.app_context():
        BabylonAssessmentProcessor(file_name='2019_CERTIFIED_ROLL',
                                   persist=True).process_babylon_pdf()
    # process_babylon_pdf('2019_TENTATIVE_ROLL_20190426')
