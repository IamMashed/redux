import logging

import pandas as pd
from sqlalchemy.exc import IntegrityError

from app import db
from app.case_management.models import CaseProperty
from config import DATA_IMPORT


class HearingProcessor:
    def __init__(self, file_name, parse_row_func, persist=True, to_file=True, ):
        self._persist = persist
        self._to_file = to_file

        self._file_name = file_name
        self._parse_func = parse_row_func

    def process(self, **kwargs):
        """
        Process scheduled hearing data

        :param kwargs: Pandas 'read_excel' function configurations
        """
        # input directory & path
        input_dir = DATA_IMPORT / 'src' / 'hearing'
        input_dir.mkdir(exist_ok=True, parents=True)
        input_path = input_dir / self._file_name

        # output directory & path
        output_dir = DATA_IMPORT / 'output' / 'hearing'
        output_dir.mkdir(exist_ok=True, parents=True)
        output_path = output_dir / f'{self._file_name[:-5]}.csv'

        df = pd.read_excel(
            input_path,
            **kwargs
        )
        df.fillna('', inplace=True)
        try:
            df = df.apply(self._parse_func, axis=1)

            if self._to_file:
                df.to_csv(output_path, index=False)

            if self._persist:
                self.update_case_hearing_data(df)

        except Exception as e:
            print(e.args)

    @staticmethod
    def update_case_hearing_data(df):
        for index, row in df.iterrows():
            apn = row['apn']
            case = CaseProperty.get_by(apn=apn)
            try:
                # update if exists only
                if case:
                    case.board_room = row.get('board_room')
                    case.hearing_date = row.get('hearing_date')
                    case.hearing_time = row.get('hearing_time')
                    case.petition_number = row.get('petition_number')
                    case.save()

                    logging.info(f'updated hearing data for the case with apn={apn}')
                else:
                    logging.warning(f'Case object not found for apn={apn}')
            except IntegrityError as e:
                db.session.rollback()
                logging.error(e.orig.args)
        return None

    @staticmethod
    def parse_hearing_info(row):
        # parse date/time object
        date_time = row[3]

        # parse hearing date
        hearing_date = date_time.date()

        # parse hearing time
        hearing_time = date_time.time()

        # parse room
        room = row[4]

        # parse petition number
        petition_number = row[5]

        # extend row with new parsed columns
        row['apn'] = row[0]
        row['hearing_date'] = hearing_date or ''
        row['hearing_time'] = hearing_time or ''
        row['board_room'] = room or ''
        row['petition_number'] = petition_number or ''

        return row[6:]

    @staticmethod
    def parse_scheduled_hearing_dates(row):
        """
        Parse hearing date row data
        """
        # parse date/time object
        date_time = row[2]

        # parse hearing date
        hearing_date = date_time.date().strftime('%m/%d/%Y')

        # parse hearing time
        hearing_time = date_time.strftime('%I:%M%p').lstrip('0')

        # parse room
        room = row[3]

        # parse petition number
        petition_number = row[4]

        # extend row with new parsed columns
        row['apn'] = row[0]
        row['hearing_date'] = hearing_date
        row['hearing_time'] = hearing_time
        row['board_room'] = room
        row['petition_number'] = petition_number

        return row[5:]

    @staticmethod
    def parse_petition_redux(row):
        """
        Parse petition redux file
        """
        petition_number = row[0]
        apn = row[1]
        board_room = row[2]
        date_time = row[3]

        # parse hearing date
        hearing_date = None
        hearing_time = None
        if date_time:
            hearing_date = str(date_time.date())

            # parse hearing time
            hearing_time = str(date_time.time())

        row['apn'] = apn
        row['hearing_date'] = hearing_date
        row['hearing_time'] = hearing_time
        row['board_room'] = board_room or ''
        row['petition_number'] = petition_number or ''

        return row[4:]
