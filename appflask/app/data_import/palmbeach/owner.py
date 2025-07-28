from pathlib import PosixPath

import pandas as pd

from app.data_import.florida import execute_task, OwnerProcessor, FloridaAssessmentOwnerProcessor
from config import DATA_IMPORT


class PalmbeachPropertyOwnerProcessor(OwnerProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(PalmbeachPropertyOwnerProcessor, self).__init__(
            provider_name='palmbeach',
            data_source='property',
            persist=persist,
            to_file=to_file,
        )
        self._file_name = file_name

    def input_dir(self) -> PosixPath:
        return DATA_IMPORT / 'src' / self.provider_name / 'property'

    def process_owner(self):
        file_path = self.input_dir() / self.file_name

        df = pd.read_csv(
            file_path,
            usecols=[
                'PROPERTY_CONTROL_NUMBER', 'OWNER_NAME', 'OWNER_ADDRESS_LINE_1',
                'OWNER_ADDRESS_LINE_2', 'OWNER_ADDRESS_LINE_3'
            ],
            low_memory=False,
            dtype=str
        )
        df.fillna('', inplace=True)
        execute_task(self.process_row, iterator=df.iterrows(), total=len(df))

    def parse_row(self, row) -> dict:
        parsed_row = dict()

        parsed_row['own_first_name'] = row.OWNER_NAME
        parsed_row['own_address_1'] = row.OWNER_ADDRESS_LINE_1
        parsed_row['own_address_2'] = row.OWNER_ADDRESS_LINE_2
        parsed_row['own_address_3'] = row.OWNER_ADDRESS_LINE_3

        parsed_row['apn'] = row.PROPERTY_CONTROL_NUMBER
        parsed_row['county'] = self.provider_name
        parsed_row['data_source'] = self.data_source
        parsed_row['created_on'] = OwnerProcessor.DEFAULT_CREATED_ON

        return parsed_row


class PalmbeachAssessmentOwnerProcessor(FloridaAssessmentOwnerProcessor):
    def __init__(self, **kwargs):
        super(PalmbeachAssessmentOwnerProcessor, self).__init__(provider_name='palmbeach', **kwargs)
