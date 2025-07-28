import threading
from concurrent.futures import as_completed, Future
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import PosixPath

import geopandas as gpd
import pandas as pd
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import create_engine
from tqdm import tqdm

from app import db
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.data_import.processor import PersistDataMixin
from app.database.models import Property, Assessment, Sale, SaleValidation, Owner, OwnerValidation
from app.database.models.assessment import AssessmentValidation, FloridaAssessmentSchema
from app.database.models.owner import OwnerSchema
from app.database.models.property import PropertyValidation, PropertyGISSchema
from app.database.models.sale import BaseSaleSchema
from app.utils.constants import County
from config import DATA_IMPORT, MAX_WORKER_COUNT, SQLALCHEMY_DATABASE_URI

FLORIDA_COUNTY_CODES = [
    ('11', 'Alachua'),
    ('12', 'Baker'),
    ('13', 'Bay'),
    ('14', 'Bradford'),
    ('15', 'Brevard'),
    ('16', 'Broward'),
    ('17', 'Calhoun'),
    ('18', 'Charlotte'),
    ('19', 'Citrus'),
    ('20', 'Clay'),
    ('21', 'Collier'),
    ('22', 'Columbia'),
    ('23', 'Miami-Dade'),
    ('24', 'DeSoto'),
    ('25', 'Dixie'),
    ('26', 'Duval'),
    ('27', 'Escambia'),
    ('28', 'Flagler'),
    ('29', 'Franklin'),
    ('30', 'Gadsden'),
    ('31', 'Gilchrist'),
    ('32', 'Glades'),
    ('33', 'Gulf'),
    ('34', 'Hamilton'),
    ('35', 'Hardee'),
    ('36', 'Hendry'),
    ('37', 'Hernando'),
    ('38', 'Highlands'),
    ('39', 'Hillsborough'),
    ('40', 'Holmes'),
    ('41', 'Indian River'),
    ('42', 'Jackson'),
    ('43', 'Jefferson'),
    ('44', 'Lafayette'),
    ('45', 'Lake'),
    ('46', 'Lee'),
    ('47', 'Leon'),
    ('48', 'Levy'),
    ('49', 'Liberty'),
    ('50', 'Madison'),
    ('51', 'Manatee'),
    ('52', 'Marion'),
    ('53', 'Martin'),
    ('54', 'Monroe'),
    ('55', 'Nassau'),
    ('56', 'Okaloosa'),
    ('57', 'Okeechobee'),
    ('58', 'Orange'),
    ('59', 'Osceola'),
    ('60', 'Palm Beach'),
    ('61', 'Pasco'),
    ('62', 'Pinellas'),
    ('63', 'Polk'),
    ('64', 'Putnam'),
    ('65', 'Saint Johns'),
    ('66', 'Saint Lucie'),
    ('67', 'Santa Rosa'),
    ('68', 'Sarasota'),
    ('69', 'Seminole'),
    ('70', 'Sumter'),
    ('71', 'Suwannee'),
    ('72', 'Taylor'),
    ('73', 'Union'),
    ('74', 'Volusia'),
    ('75', 'Wakulla'),
    ('76', 'Walton'),
    ('77', 'Washington')
]


class FileProcessor:
    """
    Base class for the file processing.
    """

    def __init__(self, provider_name: str, table: str, persist: bool = False, to_file: bool = True):
        self._provider_name = provider_name
        self._file_name = None

        assert table in ['property', 'assessment', 'sale', 'owner', 'gis', 'obsolescence']
        self._table = table

        self.persist = persist
        self.to_file = to_file

    @property
    def table(self):
        """
        Get a subdirectory of file processing.
        Can be one of ['property', 'assessment', 'sale']
        """
        return self._table

    @property
    def file_name(self):
        return self._file_name

    @property
    def provider_name(self):
        return self._provider_name

    def input_dir(self) -> PosixPath:
        """ Get the input directory path """

        if self.table is None:
            return DATA_IMPORT / 'src' / self.provider_name
        return DATA_IMPORT / 'src' / self.provider_name / self.table

    def output_dir(self) -> PosixPath:
        """ Get the output directory path """

        if self.table is None:
            return DATA_IMPORT / 'output' / self.provider_name
        return DATA_IMPORT / 'output' / self.provider_name / self.table

    def source_to_csv(self, file_name, func=None, output_path=None):
        """
        Convert source file to .csv and export it to output directory
        """
        input_path = self.input_dir() / file_name

        # callable to read source file
        if func:
            df = func(input_path)
        else:
            df = pd.read_csv(input_path)

        # output path not defined, create default
        if not output_path:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_file_name = file_name.split('.')[0]
            output_path = self.output_dir() / f'{output_file_name}.csv'

        # export
        df.to_csv(output_path, index=False)


class PoolProcessor(FileProcessor):
    """
    Class to process miamidade, broward pool data
    """

    def __init__(self, county, persist, csv, file_name):
        super(PoolProcessor, self).__init__(
            provider_name=county,
            table='property',
            persist=persist,
            to_file=csv
        )
        self._file_name = file_name

    def process_file(self):
        pass

    def output_pool_results(self, df):
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / f'{self.provider_name}_pool_data.csv', index=True, index_label='id')

        if self.persist:
            self.persist_pool_data(df)

    def persist_pool_data(self, df, create_table: bool = True, update_table: bool = True):
        try:
            table_name = f'{self.provider_name}_pool_data'
            if create_table:
                engine = create_engine(SQLALCHEMY_DATABASE_URI)
                with engine.connect() as conn, conn.begin():
                    df.to_sql(table_name, conn, "public", if_exists="replace", index_label='id')
                    print(f"Created temporary {table_name} table")

            if update_table:
                statement = f'''
                               UPDATE property
                               SET pool = {table_name}.pool
                               FROM {table_name}
                               WHERE property.apn = {table_name}.apn
                               AND property.county = '{self.provider_name}';
                                   '''

                print('updating property table')
                db.session.execute(statement)
                print("property 'pool' updated")

                drop_tmp_table_stmt = f'''DROP TABLE {table_name};'''
                db.session.execute(drop_tmp_table_stmt)
                db.session.commit()
                print('delete temporary table')

        except Exception as e:
            print(e.args)


class FloridaObsolescenceProcessor(FileProcessor):
    def __init__(self, provider_name: str, persist: bool, to_file: bool):
        super(FloridaObsolescenceProcessor, self).__init__(
            provider_name=provider_name,
            table='assessment',
            persist=persist,
            to_file=to_file
        )
        self._file_name = self._get_file_name(provider_name)

    def _get_file_name(self, county):
        if county == County.BROWARD:
            file_name = 'NAL16F201901.csv'
        elif county == County.MIAMIDADE:
            file_name = 'NAL23F201901.csv'
        elif county == County.PALMBEACH:
            file_name = 'NAL60F201902.csv'
        else:
            raise AttributeError('Invalid county name')

        return file_name

    def process_input_file(self):
        """
        Read assessment county source file and store land use codes into database.
        """
        file_path = self.input_dir() / self.file_name

        # read only parcel id and land use code columns
        df = pd.read_csv(
            file_path,
            low_memory=False,
            usecols=['PARCEL_ID', 'DOR_UC'],
            dtype={"PARCEL_ID": object, "DOR_UC": int}
        )
        df.rename(
            columns={
                'PARCEL_ID': 'apn',
                'DOR_UC': 'land_use'
            },
            inplace=True
        )
        df['county'] = self.provider_name

        # store land use code to database
        if self.persist:
            execute_task(self.process_row, iterator=df.iterrows(), total=len(df), desc=f'process {self.file_name}')

        # store land user code to csv
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / 'land_use.csv'
            df.to_csv(output_path)

    def process_row(self, row):

        from manage import app
        with app.app_context():
            try:
                Property.update_if_exists(row)
            except Exception as e:
                db.session.rollback()
                print(f'failed to update property with apn {row["apn"]} due to {e.args}')

        return None

    def analyze_land_use(self, land_use_code: int):
        file_path = self.input_dir() / self.file_name
        df = pd.read_csv(
            file_path,
            low_memory=False
        )

        # filter assessment records by land use code
        df = df[df.DOR_UC.eq(land_use_code)]

        statement = """
                SELECT property.id, property.apn, property.latitude, property.longitude, property_gis.geometry
                FROM property
                INNER JOIN property_gis ON property.id=property_gis.property_id
                WHERE property.county='{}'
                """.format(self.provider_name)

        conn = create_engine(SQLALCHEMY_DATABASE_URI)
        db_records = pd.read_sql(statement, conn)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            for i, row in df.iterrows():

                # property in database
                if str(row['PARCEL_ID']) in list(db_records['apn']):
                    new_record = (db_records[db_records.apn == str(row['PARCEL_ID'])].iloc[0]).copy()
                    output_path = self.output_dir() / (self.provider_name + '_' + str(land_use_code) + '_in_db.csv')
                    append_row_to_csv(new_record.to_dict(), output_path.as_posix())

                # property not in database
                else:
                    output_path = (self.output_dir() / (self.provider_name + '_' + str(land_use_code) +
                                                        '_not_in_db.csv'))
                    append_row_to_csv(row.to_dict(), output_path.as_posix())


class FloridaOwnerStateProcessor(FileProcessor, PersistDataMixin):
    def __init__(self, county, persist, csv):
        super(FloridaOwnerStateProcessor, self).__init__(
            provider_name=county,
            table='assessment',
            persist=persist,
            to_file=csv
        )

    def _get_files(self):
        if self.provider_name == County.BROWARD:
            return ['NAP16F201901.csv', 'NAL16F201901.csv']
        elif self.provider_name == County.MIAMIDADE:
            return ['NAP23F201901.csv', 'NAL23F201901.csv']
        elif self.provider_name == County.PALMBEACH:
            return ['NAP60F201901.csv', 'NAL60F201902.csv']
        else:
            raise ValueError('Invalid county name')

    def process_file(self, file_name):
        # files = self._get_files()
        # for file in files:
        print('Processing {}'.format(file_name))
        print('-' * 30)
        file_path = self.input_dir() / file_name

        if 'NAL' in file_name:
            apn = 'PARCEL_ID'
        elif 'NAP' in file_name:
            apn = 'ACCT_ID'
        else:
            raise ValueError("Invalid input file name")

        # read only needed cols to reduce memory usage
        df = pd.read_csv(
            file_path,
            usecols=[apn, 'OWN_STATE'],
            low_memory=False,
        )
        df.fillna('', inplace=True)
        df['county'] = self.provider_name
        df = df.astype(str)
        df.rename(columns={apn: "apn", "OWN_STATE": "state"}, inplace=True)

        if self.to_file:
            self.output_dir().mkdir(exist_ok=True, parents=True)
            df.to_csv(self.output_dir() / (file_name[:-4] + '_STATE.csv'))

        if self.persist:
            # persist prepared dataframe
            table_name = f'{self.provider_name}_{file_name[:-4].lower()}'
            schema = 'data_source'
            self._persist_states(df, table_name, schema=schema)

    def _persist_states(self, df, table_name, schema):
        try:
            self.import_data(df, table_name, schema=schema)
            db.session.execute(f"ALTER TABLE {schema}.{table_name} ADD COLUMN property_id int;")
            print("Added property_id")

            db.session.execute(
                f'''
                UPDATE {schema}.{table_name}
                SET property_id = public.property.id
                FROM public.property
                WHERE public.property.apn = {schema}.{table_name}.apn
                AND public.property.county = {schema}.{table_name}.county
                '''
            )
            print("Updated property_id")

            db.session.execute(
                f'''
                UPDATE public.owner
                SET owner_state = {schema}.{table_name}.state
                FROM {schema}.{table_name}
                WHERE public.owner.property_id = {schema}.{table_name}.property_id
                '''
            )
            print("Updated 'owner_state' in 'owner' table for {}".format(df['county'][0]))
            self.drop_data(table_name, schema)
            db.session.commit()

        except Exception as e:
            print(e.args)


class FloridaUnitProcessor(FileProcessor):
    def __init__(self, county, persist, csv):
        super(FloridaUnitProcessor, self).__init__(
            provider_name=county,
            table='property',
            persist=persist,
            to_file=csv
        )

    def process_file(self):
        try:
            if self.provider_name == County.BROWARD:
                self._process_broward_units()
            elif self.provider_name == County.MIAMIDADE:
                self._process_miamidade_units()
            elif self.provider_name == County.PALMBEACH:
                self._process_palmbeach_units("CONDO_PAS405_CERT2019_20191017.csv",
                                              "PARCEL_PAS405_CERT2019_20191017.csv")
            else:
                raise ValueError("Invalid county name for the property units processing")
        except Exception as e:
            print(e.args)

    def _persist_units(self, df):
        try:
            table_name = "units_tmp"
            engine = create_engine(SQLALCHEMY_DATABASE_URI)
            with engine.connect() as conn, conn.begin():
                df.to_sql(table_name, conn, "public", if_exists="replace", index_label='id')

            statement = '''
                UPDATE property
                SET address_unit = units_tmp.unit
                FROM units_tmp
                WHERE property.apn = units_tmp.apn
                AND property.county = units_tmp.county;
            '''

            db.session.execute(statement)
            drop_tmp_table_stmt = '''DROP TABLE units_tmp;'''
            db.session.execute(drop_tmp_table_stmt)
            db.session.commit()

        except Exception as e:
            print(e.args)

    def _process_miamidade_units(self):
        file_path = self.input_dir() / "MunRoll_00_RE_All_Properties.csv"

        # import data csv file
        from app.data_import.miamidade.property import MiamidadePropertyProcessor
        df = pd.read_csv(file_path, skiprows=4, low_memory=False, names=MiamidadePropertyProcessor.col_names)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df = df[['folio', 'land_use', 'legal2']]
        df.fillna('', inplace=True)
        df = df.astype(str)
        df.rename(columns={"folio": "apn", "legal2": "unit"}, inplace=True)

        # remove all that does not contain "UNIT"
        df = df[df.land_use.str.contains("CONDO")]
        df = df[df.unit.str.contains("UNIT")]
        df['county'] = self.provider_name

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / 'MunRoll_00_RE_All_Properties_UNITS.csv')

        if self.persist:
            self._persist_units(df)

    def _process_broward_units(self):

        file_path = self.input_dir() / "BCPA_TAX_ROLL.csv"

        # read only needed cols to reduce memory usage
        df = pd.read_csv(
            file_path,
            usecols=['FOLIO_NUMBER', 'SITUS_UNIT_NUMBER'],
            low_memory=False,
        )
        df.fillna('', inplace=True)
        df['county'] = self.provider_name
        df = df.astype(str)
        df.rename(columns={"FOLIO_NUMBER": "apn", "SITUS_UNIT_NUMBER": "unit"}, inplace=True)
        df = df[df.unit != '']

        if self.to_file:
            self.output_dir().mkdir(exist_ok=True, parents=True)
            df.to_csv(self.output_dir() / 'BCPA_TAX_ROLL_UNITS.csv')

        if self.persist:
            # persist prepared dataframe
            self._persist_units(df)

    def _process_palmbeach_units(self, *args):

        meta = {
            'file_name': '',
            'use_cols': [],
            'apn': None,
            'unit': None
        }

        for file in args:
            meta['file_name'] = file
            meta['apn'] = "PROPERTY_CONTROL_NUMBER"
            if file.startswith('CONDO'):
                meta['use_cols'] = ['PROPERTY_CONTROL_NUMBER', 'UNIT_NUMBER']
                meta['unit'] = "UNIT_NUMBER"
            elif file.startswith('PARCEL'):
                meta['use_cols'] = ['PROPERTY_CONTROL_NUMBER', 'SITUS_ADDRESS_UNIT_NUMBER']
                meta['unit'] = "SITUS_ADDRESS_UNIT_NUMBER"
            else:
                raise ValueError("Invalid input file name")

            file_path = self.input_dir() / meta['file_name']

            # read only needed cols to reduce memory usage
            df = pd.read_csv(
                file_path,
                usecols=meta['use_cols'],
                low_memory=False,
            )
            df.fillna('', inplace=True)
            df['county'] = self.provider_name
            df = df.astype(str)
            df.rename(columns={meta['apn']: "apn", meta['unit']: "unit"}, inplace=True)
            df = df[df.unit != '']

            if self.to_file:
                self.output_dir().mkdir(exist_ok=True, parents=True)
                df.to_csv(self.output_dir() / (file[:-4] + '_UNITS.csv'))

            if self.persist:
                # persist prepared dataframe
                self._persist_units(df)


class FloridaPropertyProcessor(FileProcessor):
    def __init__(self, provider_name: str, persist: bool, to_file: bool):
        super(FloridaPropertyProcessor, self).__init__(
            provider_name=provider_name,
            table='property',
            persist=persist,
            to_file=to_file
        )

    def append_to_csv(self, row):
        self.output_dir().mkdir(parents=True, exist_ok=True)
        output_file_path = self.output_dir() / self.file_name
        append_row_to_csv(row, output_file_path.as_posix())


class FloridaSaleProcessor(FileProcessor):
    def __init__(self, provider_name, file_name, persist, to_file):
        super(FloridaSaleProcessor, self).__init__(
            provider_name=provider_name,
            table='sale',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def process_input_file(self, file_path=None):
        file_path = file_path or self.input_dir() / self.file_name

        df = pd.read_csv(
            file_path,
            low_memory=False,
            dtype=str
        )
        execute_task(self.process_row, iterator=df.iterrows(), total=len(df), desc=f'process {self.file_name}')

    def process_row(self, row):
        parsed_row = self.parse_row(row)
        sale_map, error_msgs = map_row(parsed_row, BaseSaleSchema)

        if self.persist:
            commit_sale(sale_map, error_msgs)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / self.file_name
            append_row_to_csv(parsed_row, output_path.as_posix())

    def parse_row(self, data):
        parsed_row = dict()

        parsed_row['apn'] = data.PARCEL_ID
        parsed_row['county'] = self.provider_name
        parsed_row['price'] = data.SALE_PRC
        parsed_row['date'] = self.parse_sale_date(data)
        parsed_row['arms_length'] = self.parse_arms_length(data)

        return parsed_row

    @staticmethod
    def parse_sale_date(row):
        year = row.SALE_YR
        month = row.SALE_MO

        sale_date = pd.to_datetime('{}-{}'.format(year, month), dayfirst=False)
        return str(sale_date.date())

    @staticmethod
    def parse_arms_length(row):
        code = row.QUAL_CD

        if code == '':
            return None

        try:
            code = int(code)
            if code in range(1, 7):
                return True
            else:
                return False
        except ValueError:
            return None


class FloridaAssessmentProcessor(FileProcessor):
    def __init__(self, provider_name: str, nap_file_name: str, nal_file_name: str, persist: bool, to_file: bool):
        super(FloridaAssessmentProcessor, self).__init__(
            provider_name=provider_name,
            table='assessment',
            persist=persist,
            to_file=to_file
        )
        self.nap_file_name = nap_file_name
        self.nal_file_name = nal_file_name

    def is_nal(self):
        return "NAL" in self.file_name

    def is_nap(self):
        return "NAP" in self.file_name

    def process_input_file(self):

        for file_name in [self.nap_file_name, self.nal_file_name]:
            self._file_name = file_name

            file_path = self.input_dir() / self.file_name
            df = pd.read_csv(
                file_path,
                low_memory=False,
                dtype=str,
            )

            df.fillna('', inplace=True)
            execute_task(
                self.process_row,
                iterator=df.iterrows(),
                total=len(df.index),
                desc=f"process {self.file_name}"
            )

    def process_row(self, row):
        parsed_row = self.parse_row(row)

        assmnt_map, errors = map_row(parsed_row, FloridaAssessmentSchema)
        if self.persist:
            commit_assessment(assmnt_map, errors)

            # update 'city' column in 'property' table
            data = {
                'apn': parsed_row.get('apn'),
                'county': parsed_row.get('county'),
                'city': parsed_row.get('city')
            }
            from manage import app
            with app.app_context():
                Property.update_if_exists(data)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / self.file_name
            append_row_to_csv(parsed_row, output_path.as_posix())

    def parse_row(self, row):
        parsed_row = dict()
        if self.is_nal():
            parsed_row = self._parse_nal(row)
        elif self.is_nap():
            parsed_row = self._parse_nap(row)

        # parsed_row['assessment_date'] = str(pd.to_datetime(row.ASMNT_YR).date())
        parsed_row['county'] = self.provider_name
        parsed_row['city'] = row.PHY_CITY

        return parsed_row

    def _parse_nal(self, row):
        parsed_row = dict()
        parsed_row['apn'] = row.PARCEL_ID
        parsed_row['assessment_type'] = "final"
        parsed_row['value'] = row.JV

        return parsed_row

    def _parse_nap(self, row):
        parsed_row = dict()

        parsed_row['apn'] = row.ACCT_ID
        parsed_row['assessment_type'] = "final"
        parsed_row['value'] = row.AV_TOTAL

        return parsed_row


class GISProcessor(FileProcessor):
    def __init__(self, provider_name, persist, to_file):
        super(GISProcessor, self).__init__(
            provider_name=provider_name,
            table='gis',
            persist=persist,
            to_file=to_file
        )
        self.include_xy = True

    def process_row(self, row):
        # parse gis row
        parsed_row = self.parse_row(row)

        # map GIS data with marshmallow schema
        gis_map, error_msgs = map_row(parsed_row, PropertyGISSchema)

        # export to db
        if self.persist:
            commit_property_gis(gis_map, error_msgs, include_xy=self.include_xy)

        # export to csv
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / (self.file_name[:-4] + '.csv')
            append_row_to_csv(parsed_row, output_path.as_posix())

    def parse_row(self, row) -> dict:
        pass

    @staticmethod
    def parse_label_coordinates(row):
        parsed_row = dict()

        parsed_row['longitude'] = row.lat_long_geometry.x
        parsed_row['latitude'] = row.lat_long_geometry.y

        parsed_row['coordinate_x'] = row.xy_geometry.x
        parsed_row['coordinate_y'] = row.xy_geometry.y

        return parsed_row

    @staticmethod
    def parse_polygon_coordinates(row):
        parsed_row = dict()

        # get centered polygon x, y coordinates
        parsed_row['longitude'] = row.lat_long_geometry.centroid.x
        parsed_row['latitude'] = row.lat_long_geometry.centroid.y

        parsed_row['coordinate_x'] = row.xy_geometry.centroid.x
        parsed_row['coordinate_y'] = row.xy_geometry.centroid.y

        return parsed_row


class OwnerProcessor(FileProcessor):
    DEFAULT_CREATED_ON = '2000-01-01'

    def __init__(self, provider_name, data_source, persist, to_file):
        super(OwnerProcessor, self).__init__(
            provider_name=provider_name,
            table='owner',
            persist=persist,
            to_file=to_file
        )
        self.data_source = data_source

    def process_row(self, row):
        # parse gis row
        parsed_row = self.parse_row(row)

        # map owner data with marshmallow schema
        owner_map, errors = map_row(parsed_row, OwnerSchema)

        # export to db
        if self.persist:
            commit_owner(owner_map, errors)

        # export to csv
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / '{}_{}_owners.csv'.format(self.provider_name, self.data_source)
            append_row_to_csv(parsed_row, output_path.as_posix())

    def parse_row(self, row) -> dict:
        pass


class FloridaAssessmentOwnerProcessor(OwnerProcessor):
    def __init__(self, nap_file_name: str, nal_file_name: str, provider_name: str, persist: bool, to_file: bool):
        super(FloridaAssessmentOwnerProcessor, self).__init__(
            provider_name=provider_name,
            data_source='assessment',
            persist=persist,
            to_file=to_file,
        )
        self.nap_file_name = nap_file_name
        self.nal_file_name = nal_file_name

    def input_dir(self) -> PosixPath:
        return DATA_IMPORT / 'src' / self.provider_name / 'assessment'

    def process_owner(self):
        for file_name in [self.nap_file_name, self.nal_file_name]:
            self._file_name = file_name

            file_path = self.input_dir() / self.file_name
            df = pd.read_csv(
                file_path,
                usecols=self._get_use_cols(),
                low_memory=False,
                dtype=str,
            )
            df.fillna('', inplace=True)

            execute_task(
                self.process_row,
                iterator=df.iterrows(),
                total=len(df.index),
            )

    def _get_use_cols(self):
        if self.is_nap():
            return [
                'ACCT_ID', 'ASMNT_YR', 'OWN_ADDR', 'OWN_NAM', 'OWN_CITY', 'OWN_ZIPCD', 'OWN_STATE'
            ]
        elif self.is_nal():
            return [
                'PARCEL_ID', 'ASMNT_YR', 'OWN_ADDR1', 'OWN_ADDR2', 'OWN_CITY', 'OWN_ZIPCD', 'OWN_NAME', 'OWN_STATE'
            ]

    def is_nal(self):
        return "NAL" in self.file_name

    def is_nap(self):
        return "NAP" in self.file_name

    def parse_row(self, row) -> dict:
        parsed_row = dict()
        if self.is_nal():
            parsed_row = self._parse_nal_owner(row)
        elif self.is_nap():
            parsed_row = self._parse_nap_owner(row)

        parsed_row['data_source'] = self.data_source
        parsed_row['county'] = self.provider_name
        parsed_row['own_state'] = row.OWN_STATE

        return parsed_row

    def _parse_nal_owner(self, row):
        parsed_row = dict()
        parsed_row['own_address_1'] = row.OWN_ADDR1
        parsed_row['own_address_2'] = row.OWN_ADDR2
        parsed_row['own_city'] = row.OWN_CITY
        parsed_row['own_zip'] = self.parse_zip(row)

        parsed_row['apn'] = row.PARCEL_ID
        parsed_row['created_on'] = str(pd.to_datetime(row.ASMNT_YR).date())

        if ',' in row.OWN_NAME:
            parsed_row['own_first_name'] = row.OWN_NAME.split(',')[0].strip()
            parsed_row['own_last_name'] = row.OWN_NAME.split(',')[1].strip()
        else:
            parsed_row['own_first_name'] = row.OWN_NAME

        return parsed_row

    def _parse_nap_owner(self, row):
        parsed_row = dict()
        parsed_row['own_address_1'] = row.OWN_ADDR
        parsed_row['own_city'] = row.OWN_CITY
        parsed_row['own_zip'] = self.parse_zip(row)

        parsed_row['apn'] = row.ACCT_ID
        parsed_row['created_on'] = str(pd.to_datetime(row.ASMNT_YR).date())

        if ',' in row.OWN_NAM:
            parsed_row['own_first_name'] = row.OWN_NAM.split(',')[0].strip()
            parsed_row['own_last_name'] = row.OWN_NAM.split(',')[1].strip()
        else:
            parsed_row['own_first_name'] = row.OWN_NAM

        return parsed_row

    @staticmethod
    def parse_zip(row):
        if row.OWN_ZIPCD is None or row.OWN_ZIPCD == "":
            return None
        try:
            return int(row.OWN_ZIPCD)
        except ValueError:
            return None


def map_row(row_data: dict, mapping_schema):
    """
    Map row data with  specified marshmallow Schema.
    """

    # validate raw with marshmallow Schema
    error_msgs = None
    try:
        fields_map = mapping_schema(unknown=EXCLUDE).load(row_data)
    except ValidationError as e:
        error_msgs = e.messages
        fields_map = e.valid_data

    return fields_map, error_msgs


def _commit(fields_map, model, validation_model, errors=None, upsert=False):
    if errors is None:
        errors = dict()

    apn = fields_map.pop('apn')
    county = fields_map.pop('county')

    from manage import app
    with app.app_context():
        prop = Property.query.filter_by(apn=apn, county=county).first()

        if not prop:
            errors['property'] = f'property with apn {apn} not in database'
        else:
            fields_map['property_id'] = prop.id
            if upsert:
                insert_error = model.upsert(fields_map)
            else:
                insert_error = model.insert(fields_map)
                print(f'inserted with property id {prop.id}')
            if insert_error:
                errors['database_operation'] = insert_error

        # if errors and fields_map:
        #     validation_model.insert(apn, county, errors)

    return None


def commit_assessment(fields_map, errors=None, upsert=False):
    return _commit(fields_map, Assessment, AssessmentValidation, errors, upsert)


def commit_sale(fields_map, errors=None, upsert=True):
    return _commit(fields_map, Sale, SaleValidation, errors, upsert)


def commit_owner(fields_map, errors=None, upsert=False):
    return _commit(fields_map, Owner, OwnerValidation, errors, upsert)


def commit_property(fields_map, errors=None):
    """ Store property into database """

    if errors is None:
        errors = dict()

    apn = fields_map.get('apn')
    county = fields_map.get('county')

    from manage import app
    with app.app_context():
        insert_error = Property.insert(fields_map)

        if insert_error:
            errors['database_operation'] = insert_error

        # if any errors during validation, store them
        # in the database PropertyValidation table
        if errors and fields_map:
            PropertyValidation.insert(apn, county, errors)

        db.session.commit()


def commit_property_gis(row, errors=None, include_xy=True):
    if errors is None:
        errors = dict()

    apn = row.get('apn')
    county = row.get('county')

    latitude = row.get('latitude')
    longitude = row.get('longitude')

    from manage import app
    with app.app_context():
        prop = Property.query.filter_by(apn=apn, county=county).first()
        if not prop:
            errors['GIS'] = f'property with apn {apn} not in database'
        else:
            update_prop = dict(
                    apn=prop.apn,
                    county=prop.county,
                    latitude=latitude,
                    longitude=longitude
                )
            if include_xy:
                update_prop['coordinate_x'] = row.get('coordinate_x')
                update_prop['coordinate_y'] = row.get('coordinate_y')
            update_error = Property.update_if_exists(update_prop)

            if update_error:
                errors['database_operation'] = update_error

        if errors:
            PropertyValidation.insert(apn, county, errors)
    return None


def read_shp(file_path):
    gdf = gpd.GeoDataFrame.from_file(file_path)
    # print(gdf.crs)
    gdf = gdf[~gdf.geometry.isna()]
    # save geometry as x,y points
    gdf['xy_geometry'] = gdf['geometry']

    # convert to latitude/longitude coordinate reference system
    gdf.to_crs(epsg=4326, inplace=True)
    gdf.rename(columns={'geometry': 'lat_long_geometry'}, inplace=True)

    return gdf


def execute_task(task, iterator, concurrency=MAX_WORKER_COUNT, **kwargs):
    """
    The method executes the 'task' for each iterator element in multi-processed mode.

    :param task: function to execute
    :param iterator: iterator to process row by row
    :param concurrency: max count of workers
    :param kwargs: passed to config progress bar
    """
    with ProcessPoolExecutor(concurrency) as executor:
        futures = {executor.submit(task, row): row for index, row in iterator}
        print('tasks submitted')
        pbar = tqdm(**kwargs)
        for future in as_completed(futures):
            pbar.update(1)
            try:
                _ = future.result() # noqa
                del futures[future]
            except Exception as exc:
                print(exc)


def task_queue(task, iterator, concurrency=10, on_fail=lambda _: None, **kwargs):
    """
    Alternative method to execute task , that do not grow memory usage
    """
    def submit():
        try:
            # get next row
            obj = next(iterator)
        except StopIteration:
            return
        if result.cancelled():
            return

        future = executor.submit(task, obj[1])
        future.obj = obj
        future.add_done_callback(parse_done)

    def parse_done(future):
        pbar.update(1)
        # when task done, submit next one
        submit()

        if future.exception():
            on_fail(future.exception(), future.obj)

    def cleanup(_):
        with io_lock:
            executor.shutdown(wait=False)

    io_lock = threading.RLock()
    executor = ThreadPoolExecutor(concurrency)

    pbar = tqdm(**kwargs)
    result = Future()
    result.add_done_callback(cleanup)

    with io_lock:
        # submit first tasks of 'concurrency' threads
        for _ in range(concurrency):
            submit()

    return result
