from pathlib import PosixPath

import pandas as pd

from app.data_import.florida import OwnerProcessor, execute_task, FloridaAssessmentOwnerProcessor
from config import DATA_IMPORT


class BrowardPropertyOwnerProcessor(OwnerProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(BrowardPropertyOwnerProcessor, self).__init__(
            provider_name='broward',
            data_source='property',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def input_dir(self) -> PosixPath:
        return DATA_IMPORT / 'src' / self.provider_name / 'property'

    def process_owner(self):
        file_path = self.input_dir() / self.file_name

        # read only needed cols to reduce memory usage
        df = pd.read_csv(
            file_path,
            usecols=[
                'FOLIO_NUMBER', 'NAME_LINE_1', 'NAME_LINE_2', 'ADDRESS_LINE_1', 'ADDRESS_LINE_2', 'CITY', 'ZIP',
                'ACTUAL_YEAR_BUILT'
            ],
            low_memory=False,
            dtype=str
        )
        df.fillna('', inplace=True)
        execute_task(self.process_row, iterator=df.iterrows(), total=len(df))

    def parse_row(self, row) -> dict:
        parsed_row = dict()

        if ',' in row.NAME_LINE_1:
            parsed_row['own_first_name'] = row.NAME_LINE_1.split(',')[0].strip()
            parsed_row['own_last_name'] = row.NAME_LINE_1.split(',')[1].strip()
        else:
            parsed_row['own_first_name'] = row.NAME_LINE_1

        if ',' in row.NAME_LINE_2:
            parsed_row['own_second_owner_first_name'] = row.NAME_LINE_2.split(',')[0].strip()
            parsed_row['own_second_owner_last_name'] = row.NAME_LINE_2.split(',')[1].strip()
        else:
            parsed_row['own_second_owner_first_name'] = row.NAME_LINE_2

        parsed_row['own_address_1'] = row.ADDRESS_LINE_1
        parsed_row['own_address_2'] = row.ADDRESS_LINE_2
        parsed_row['own_city'] = row.CITY
        parsed_row['own_zip'] = self.parse_zip(row)

        parsed_row['apn'] = row.FOLIO_NUMBER
        parsed_row['county'] = self.provider_name
        parsed_row['data_source'] = self.data_source
        parsed_row['created_on'] = self.parse_created_on(row)

        return parsed_row

    @staticmethod
    def parse_created_on(data):
        if data.ACTUAL_YEAR_BUILT == '' or data.ACTUAL_YEAR_BUILT == '0':
            return OwnerProcessor.DEFAULT_CREATED_ON
        try:
            dt = pd.to_datetime(str(data.ACTUAL_YEAR_BUILT))
            return str(dt.date())
        except ValueError:
            return OwnerProcessor.DEFAULT_CREATED_ON

    @staticmethod
    def parse_zip(data):
        try:
            return int(data.ZIP)
        except ValueError:
            return None


class BrowardAssessmentOwnerProcessor(FloridaAssessmentOwnerProcessor):
    def __init__(self, **kwargs):
        super(BrowardAssessmentOwnerProcessor, self).__init__(provider_name='broward', **kwargs)
