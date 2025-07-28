import pandas as pd
from pathlib import PosixPath

from app.data_import.florida import OwnerProcessor, execute_task, FloridaAssessmentOwnerProcessor
from app.data_import.miamidade.property import MiamidadePropertyProcessor
from config import DATA_IMPORT


class MiamidadePropertyOwnerProcessor(OwnerProcessor):
    def __init__(self, file_name: str, persist: bool, data_source, to_file: bool, created_on=None):
        super(MiamidadePropertyOwnerProcessor, self).__init__(
            provider_name='miamidade',
            data_source=data_source,
            persist=persist,
            to_file=to_file
        )
        self._created_on = created_on
        self._file_name = file_name

    def input_dir(self) -> PosixPath:
        return DATA_IMPORT / 'src' / self.provider_name / self.data_source

    def process_owner(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(
            file_path,
            names=MiamidadePropertyProcessor.col_names,
            usecols=[
                'folio', 'yearbuilt', 'owner1', 'owner2', 'mailing_address', 'mailing_city', 'mailing_zip',
                'mailing_state'
            ],
            skiprows=4,
            low_memory=False,
            dtype=str
        )

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df.fillna('', inplace=True)

        execute_task(self.process_row, iterator=df.iterrows(), total=len(df))

    def parse_row(self, row) -> dict:
        parsed_row = dict()

        parsed_row['own_first_name'] = row.owner1
        parsed_row['own_second_owner_first_name'] = row.owner2
        parsed_row['own_address_1'] = row.mailing_address
        parsed_row['own_city'] = row.mailing_city
        parsed_row['own_zip'] = self.parse_zip(row)
        parsed_row['own_state'] = row.mailing_state

        parsed_row['apn'] = row.folio
        parsed_row['county'] = self.provider_name
        parsed_row['data_source'] = self.data_source
        parsed_row['created_on'] = self._created_on or self.parse_created_on(row)

        return parsed_row

    @staticmethod
    def parse_zip(row):
        if row.mailing_zip == "":
            return None
        try:
            return int(row.mailing_zip[0:5])
        except ValueError:
            return None

    @staticmethod
    def parse_created_on(data):
        try:
            age = int(data.yearbuilt)
            if age == 0 or age > 2020:
                return OwnerProcessor.DEFAULT_CREATED_ON
            dt = pd.to_datetime(str(age))
            return str(dt.date())
        except ValueError:
            return OwnerProcessor.DEFAULT_CREATED_ON


class MiamidadeAssessmentOwnerProcessor(FloridaAssessmentOwnerProcessor):
    def __init__(self, **kwargs):
        super(MiamidadeAssessmentOwnerProcessor, self).__init__(provider_name='miamidade', **kwargs)
