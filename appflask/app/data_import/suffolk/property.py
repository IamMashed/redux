from concurrent.futures import as_completed, ProcessPoolExecutor
from enum import Enum
import concurrent.futures
import click

from marshmallow import EXCLUDE, ValidationError
from tqdm import tqdm

from app import db
from app.data_import.florida import GISProcessor, read_shp, FileProcessor
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.data_import.processor import ProcessorOperation, ProcessorSettings, PersistDataMixin
from app.data_import.suffolk import queries

from app.database.models.property import (
    Property,
    PropertyValidation,
    SuffolkPropertySchema)

import pandas as pd

from app.utils.comp_utils import is_whitelisted
from app.utils.constants import BASEMENT_TYPE_MAP, County, PROPERTY_STYLE_MAP
from app.utils.fix_address import capitalize_address
from config import DATA_IMPORT, MAX_WORKER_COUNT

pd.options.mode.chained_assignment = None  # default='warn'


class Fips(Enum):
    broward = 12011
    miami_dade = 12086
    palm_beach = 12099
    nassau = 36059
    suffolk = 36103


class SuffolkPropertyAddressProcessor(FileProcessor):
    def __init__(self, file_name, persist, csv):
        super(SuffolkPropertyAddressProcessor, self).__init__(
            provider_name='suffolk',
            table='property',
            persist=persist,
            to_file=csv
        )
        self._file_name = file_name

    def prepare_df(self, df):
        df['state'] = 'NY'
        df = df[pd.notna(df['par_id'])]
        df.fillna('', inplace=True)

        df['loc_st_nbr'] = df['loc_st_nbr'].astype(str)
        df['loc_st_name'] = df['loc_st_name'].astype(str)
        df['loc_mail_st_suff'] = df['loc_mail_st_suff'].astype(str)

        df['loc_st_nbr'] = df['loc_st_nbr'].apply(lambda x: x.strip())
        df['loc_st_name'] = df['loc_st_name'].apply(lambda x: x.strip())
        df['loc_mail_st_suff'] = df['loc_mail_st_suff'].apply(lambda x: x.strip())

        df['addr_line_1'] = df[['loc_st_nbr', 'loc_st_name', 'loc_mail_st_suff']].agg(' '.join, axis=1)
        df['addr_line_3'] = df[['loc_muni_name', 'state', 'loc_zip']].agg(' '.join, axis=1)
        df['address'] = df[['addr_line_1', 'addr_line_3']].agg(', '.join, axis=1).str.strip(',')

        df = df[['loc_st_nbr', 'loc_st_name', 'loc_mail_st_suff', 'addr_line_1', 'addr_line_3', 'address', 'par_id']]
        df['addr_line_1'] = df['addr_line_1'].apply(lambda x: capitalize_address(x))
        df['addr_line_3'] = df['addr_line_3'].apply(lambda x: capitalize_address(x))
        df['address'] = df['address'].apply(lambda x: capitalize_address(x))

        return df

    def process(self):
        input_path = self.input_dir() / self.file_name
        self.output_dir().mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir() / f'addresses_{self.file_name[:-4]}.csv'

        df = pd.read_csv(
            input_path,
            dtype=str,
            usecols=['par_id', 'loc_st_nbr', 'loc_st_name', 'loc_mail_st_suff', 'loc_unit_name', 'loc_unit_nbr',
                     'loc_muni_name', 'loc_zip']
        )
        df = self.prepare_df(df)
        if self.to_file:
            df.to_csv(output_path)


class Processor(FileProcessor, PersistDataMixin):
    """
    Processing unified data source that will cover all except
    assessment and photographs
    """

    def __init__(self, folder_name, settings: ProcessorSettings):
        """
        :param folder_name: unified data txt file
        :param settings: Processor settings
        """
        super(Processor, self).__init__(provider_name=County.SUFFOLK, table='property', persist=settings.persist,
                                        to_file=settings.to_file)
        self.folder_name = folder_name
        self.settings = settings
        self.schema = SuffolkPropertySchema(unknown=EXCLUDE)

    # noinspection DuplicatedCode
    @staticmethod
    def commit(property_map, errors, operation=ProcessorOperation.UPDATE_IF_EXISTS, persist_errors=False):
        # handle insert new or update existed operation
        if operation == ProcessorOperation.UPSERT:
            obj = Property.query.filter_by(apn=property_map['apn'], county=property_map['county'])
            if obj.first():
                operation_errors = Property.update(obj, property_map)
            else:
                operation_errors = Property.insert(property_map)
        # handle update existed operation
        elif operation == ProcessorOperation.UPDATE_IF_EXISTS:
            operation_errors = Property.update_if_exists(property_map)

        # handle insert operation
        elif operation == ProcessorOperation.INSERT:
            operation_errors = Property.insert(property_map)
        else:
            raise Exception('Invalid database operation')

        if persist_errors:
            if operation_errors:
                errors['database_operation'] = operation_errors

            if errors and property_map:
                PropertyValidation.insert(apn=property_map['apn'],
                                          county=property_map['county'],
                                          errors=errors)

    def map_row(self, raw_data):
        # raw_data_ = raw_data.to_dict()
        raw_data_ = raw_data._asdict()
        # raw_data__ = {x: y.strip() for x, y in raw_data_.items()}
        error_messages = dict()
        property_map = {}
        try:
            property_map = self.schema.load(raw_data_)
        except ValidationError as e:
            error_messages = e.messages
            property_map = e.valid_data
        finally:
            property_map['is_residential'] = is_whitelisted(**property_map)
            property_map['address'] = capitalize_address(property_map['address'])
            property_map['address_line_1'] = capitalize_address(property_map['address_line_1'])
            property_map['address_line_2'] = capitalize_address(property_map['address_line_2'])
            property_map['street'] = capitalize_address(property_map['street'])
            property_map['town'] = capitalize_address(property_map['town'])

        # store record to database
        if self.settings.persist:
            from manage import app
            with app.app_context():
                Processor.commit(property_map, error_messages, self.settings.operation)

        if self.settings.to_file:
            output_folder = DATA_IMPORT / 'output' / 'suffolk' / 'property'
            output_folder.mkdir(parents=True, exist_ok=True)
            output_path = output_folder / 'suffolk_property.csv'

            append_row_to_csv(property_map, output_path.as_posix())

        return property_map

    def join_dataframes(self):
        """Join all the property sources into one dataframe"""
        first = DATA_IMPORT / 'src' / self.folder_name / 'property' / 'Suff_Priv_Inv.csv'
        first_df = pd.read_csv(first,
                               usecols=['APN',
                                        'STYLE',
                                        'LOT_SIZE',
                                        'LOT_SQFT',
                                        'GLA',
                                        'AGE',
                                        'BASEMENT',
                                        'BATHS',
                                        'GARAGE',
                                        'ROOMS',
                                        'BEDROOMS',
                                        'KITCHENS',
                                        'POOL',
                                        'POOL_TYPE',
                                        'WATERFRONT',
                                        'FIREPLACES'],
                               dtype='str')
        first_df['APN'] = first_df['APN'].apply(lambda x: str(x).strip())

        second = DATA_IMPORT / 'src' / 'suffolk' / 'property' / 'parcel_parid.csv'
        second_df = pd.read_csv(second,
                                usecols=[
                                    'par_id',
                                    'parcel_id',
                                    'sec',
                                    'block',
                                    'lot',
                                    'muni_code',
                                    'dist_cd'
                                ],
                                dtype='str')
        df = pd.merge(first_df, second_df, how='left', left_on='APN', right_on='par_id')

        third = DATA_IMPORT / 'src' / 'suffolk' / 'property' / 'parcel.txt'
        third_df = SuffolkPropertyProcessor.read_parcel(file_path=third)
        third_df = third_df.replace({pd.np.nan: ''})

        df = pd.merge(df, third_df, how='left', on=['parcel_id', 'muni_code'])

        # constructing muni_code to match sale data
        # df.muni_code = df.muni_code.fillna(0).astype(int)
        # df.swis_vlg = df.swis_vlg.fillna(0).astype(int)
        # df.muni_code = df.muni_code + df.swis_vlg
        # df.muni_code = df.muni_code.astype(str)
        # del df['swis_vlg']

        return df

    def parse_basement_type(self, value):
        """
        Parse basement type value
        """
        if not value:
            return None

        for key, name in BASEMENT_TYPE_MAP['suffolk'].items():
            if name == value.lower().strip():
                return key
        return None

    def parse_full_baths(self, value):
        """
        Parse full baths value
        """
        if not value:
            return None

        split = str(value).strip().split('.')
        return int(split[0].strip()) if split and split[0] else None

    def parse_half_baths(self, value):
        """
        Parse half baths value
        """
        if not value:
            return None

        split = str(value).strip().split('.')
        return 1 if len(split) > 1 and int(split[1].strip()) == 5 else None

    def parse_pool(self, value):
        """
        Parse pool value
        """
        value = value.strip()

        if value == 'Y':
            return True
        elif value == 'N':
            return False

        return None

    def parse_waterfront(self, value):
        """
        Parse waterfront value
        """
        value = value.strip()

        if value == 'Y':
            return True
        elif value == 'N':
            return False

        return None

    def parse_zip(self, value):
        """
        Parse zip value
        """
        value = value.strip()
        if not value:
            return None

        return value[:5]

    def parse_address(self, row):
        """
        Parse address fields
        """
        number = row['number'].strip()
        street = row['street'].strip()
        suffix = row['loc_mail_st_suff'].strip()
        town = row['town'].strip()

        state = 'NY'
        zip_code = row['zip'] or ''

        unit_name = row['loc_unit_name'].strip()
        unit_number = row['loc_unit_nbr'].strip()

        address_line_1 = ' '.join([number, street, suffix]).strip()
        address_line_2 = ' '.join([unit_name, unit_number]).strip()
        address_line_3 = ' '.join([town, state, zip_code]).strip()

        row['address_line_1'] = address_line_1
        row['address_line_2'] = address_line_2

        address = address_line_1
        if address_line_2:
            address = ', '.join([address, address_line_2, address_line_3])
        else:
            address = ', '.join([address, address_line_3])
        row['address'] = address.strip(',')

        return row

    def process(self):
        df = self.join_dataframes()
        df = df[pd.notna(df['par_id'])]
        df = df.replace({pd.np.nan: ''})

        df.rename(
            columns={
                'APN': "apn",
                "STYLE": "property_style",
                "LOT_SIZE": "lot_size",
                "LOT_SQFT": "lot_size_sqft",
                "GLA": "gla_sqft",
                "AGE": "age",
                "BASEMENT": "basement_type",
                "GARAGE": "garages",
                "ROOMS": "rooms",
                "BEDROOMS": "bedrooms",
                "KITCHENS": "kitchens",
                "POOL": "pool",
                "WATERFRONT": "waterfront",
                "FIREPLACES": "fireplaces",
                "grid_east": "coordinate_x",
                "grid_north": "coordinate_y",
                "loc_st_nbr": "number",
                "loc_st_name": "street",
                "loc_muni_name": "town",
                "loc_zip": "zip",
                "sec": "section",
                "block": "block",
                "lot": "lot",
                "dist_cd": "district"
            },
            inplace=True
        )

        # parse columns
        df['basement_type'] = df['basement_type'].apply(self.parse_basement_type)
        df['full_baths'] = df['BATHS'].apply(self.parse_full_baths)
        df['half_baths'] = df['BATHS'].apply(self.parse_half_baths)
        df['pool'] = df['pool'].apply(self.parse_pool)
        df['waterfront'] = df['waterfront'].apply(self.parse_waterfront)
        df['zip'] = df['zip'].apply(self.parse_zip)

        # capitalize
        df['street'] = df['street'].apply(capitalize_address)
        df['loc_mail_st_suff'] = df['loc_mail_st_suff'].apply(capitalize_address)
        df['loc_unit_name'] = df['loc_unit_name'].apply(capitalize_address)
        df['town'] = df['town'].apply(capitalize_address)

        # parse address, address_line_1, address_line_2, (takes time)
        df = df.apply(self.parse_address, axis=1)

        df.drop(['BATHS', 'POOL_TYPE', 'par_id', 'swis_vlg'], axis=1, inplace=True)

        if self.settings.to_file:
            output_folder = DATA_IMPORT / 'output' / 'suffolk' / 'property'
            output_folder.mkdir(parents=True, exist_ok=True)
            output_path = output_folder / 'suff_output_priv_inv.csv'
            df.to_csv(output_path, index=False)

    def process_input_file(self):
        output_df = pd.DataFrame()
        joined_df = self.join_dataframes()
        joined_df = joined_df[pd.notna(joined_df['par_id'])]
        joined_df = joined_df.replace({pd.np.nan: ''})
        print('joined frames...')

        # execute_task(
        #     task=self.map_row,
        #     iterator=joined_df.iterrows(),
        #     total=len(joined_df),
        #     desc=f'process Suff_Priv_Inv.csv'
        # )
        with concurrent.futures.ThreadPoolExecutor(MAX_WORKER_COUNT) as executor:
            futures = []
            with click.progressbar(length=joined_df.shape[0],
                                   label='step 1 / 2...') as bar:
                for row in joined_df.itertuples():
                    bar.update(1)
                    futures.append(executor.submit(self.map_row, row))
            with click.progressbar(length=joined_df.shape[0],
                                   label='step 2 / 2...') as bar:
                for future in as_completed(futures):
                    bar.update(1)
                    if self.settings.to_file:
                        output_df = output_df.append(future.result(),
                                                     ignore_index=True)

        if self.settings.to_file:
            output_folder = DATA_IMPORT / 'output' / 'suffolk' / 'property'
            output_folder.mkdir(parents=True, exist_ok=True)
            output_path = output_folder / 'suffolk_property.csv'
            output_df.to_csv(output_path, index=False)
        return None


class SuffolkGISProcessor(GISProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super().__init__('suffolk', persist, to_file)
        self._file_name = file_name
        self.include_xy = False

    def parse_row(self, row):
        parsed_row = dict()

        parsed_row['apn'] = row.PARCELID
        parsed_row['county'] = self.provider_name
        parsed_row.update(self.parse_polygon_coordinates(row))

        return parsed_row

    def process_gis_zip(self):
        gis_path = self.input_dir() / self.file_name
        gdf = read_shp('zip://' + gis_path.as_posix())

        with ProcessPoolExecutor(MAX_WORKER_COUNT) as executor:
            futures = [executor.submit(self.process_row, row[1]) for row in gdf.iterrows()]
            print('tasks submitted')
            pbar = tqdm(total=gdf.shape[0])
            for future in as_completed(futures):
                pbar.update(1)
                try:
                    _ = future.result()  # noqa
                except Exception as exc:
                    print(exc)

        # update geo column in property table using parsed latitude/longitude
        if self.persist:
            from app import db
            try:
                db.session.execute(
                    f'''
                        UPDATE property
                        SET geo = ST_SetSRID(ST_MakePoint(longitude::numeric, latitude::numeric), 4326)
                        WHERE geo IS NULL
                        AND latitude IS NOT NULL
                        AND longitude IS NOT NULL
                        AND county='{self.provider_name}';
                    '''
                )
                db.session.commit()
                print("Updated property geo")
            except Exception as e:
                db.session.rollback()
                print(e.args)
            finally:
                db.session.close()
        return None


class SuffolkPropertyProcessor(FileProcessor, PersistDataMixin):
    """
    Class implementation to process Suffolk parcel.txt, res_bld.txt files.
        - parcel.txt file contains parcel information (number, street, zip, section, block, lot, etc.)
        - res_bldg.txt file contains inventory fields (baths, bedrooms, kitchens, etc.)
    """

    def __init__(self, settings: ProcessorSettings):
        super(SuffolkPropertyProcessor, self).__init__(
            provider_name=County.SUFFOLK,
            table='property',
            persist=settings.persist,
            to_file=settings.to_file
        )
        self.settings = settings

    def process(self):
        """
        Choose processing by database operation:
            - update: to update fields
            - insert: to insert all fields
            - insert new: to insert only not existed ones
            etc.
        """
        if self.settings.operation == ProcessorOperation.UPDATE:
            self.process_update()
        elif self.settings.operation == ProcessorOperation.INSERT:
            pass

    def process_update(self):
        """
        When new data sources come, we need to update existed data in database.
        The Entry point to update processing.
        According to input settings ability to save into .csv file or persist into changes to database.

        Required data sources:
            - 'parcel.txt'
            - 'Swis.xlsx'
            - res_bldg.txt

        Input Dir Path: /data_import/src/suffolk/property

        Instructions:
            - read parcel.txt into memory and parse
            - read Suffolk Swis.xlsx as it is
            - import two dataframes into database 'data_source' schema
            - perform a call of set of sql queries, transformed from the input .sql file to create parcel_parid table
            - perform update parcel & inventory fields
        """
        # first we need to read all required data from parcel.txt & parse
        parcel = self.read_parcel(file_path=self.input_dir() / 'parcel.txt')
        parcel = self.parse_parcel(parcel)

        # read data from 'Suffolk Swis.xlsx' file
        # this is a 'swis.txt' table missed in input data source set and requested as additional file
        # we use this table to join with parcel.txt and for the parcel_parid creation (apn)
        swis = self.read_swis(file_path=self.input_dir() / 'Suffolk Swis.xlsx')

        # read inventories data from 'res_bldg.txt' file
        # parse 'property_style' translations
        res_bldg = self.read_res_bldg(file_path=self.input_dir() / 'res_bldg.txt')
        res_bldg = self.parse_res_bldg(res_bldg)

        # export results to file system
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            parcel.to_csv(self.output_dir() / 'suffolk_parcel.csv', index=False)
            swis.to_csv(self.output_dir() / 'suffolk_swis.csv', index=False)
            res_bldg.to_csv(self.output_dir() / 'suffolk_res_bldg.csv', index=False)

        # export results to DB
        if self.persist:
            parcel_table = 'suffolk_parcel'
            swis_table = 'suffolk_swis'
            parcel_parid_table = 'suffolk_parcel_parid'
            res_bldg_table = 'suffolk_res_bldg'
            schema = 'data_source'

            # import parcel.txt, swis.txt into database
            # the parcel.txt is huge and it take ~15-20 minutes to import all the data to table
            self.import_data(parcel, table_name=parcel_table, schema=schema, chunksize=20000)
            self.import_data(swis, table_name=swis_table, schema=schema, chunksize=20000)
            self.import_data(res_bldg, table_name=res_bldg_table, schema=schema, chunksize=20000)
            self.create_parcel_parid(table_name=parcel_parid_table, schema=schema)

            # commit 'suffolk_parcel_parid' table
            db.session.commit()

            # update parcel fields
            self.update_parcel()

            # update inventory fields
            self.update_resbld()

            # clean imported tables from database
            if self.settings.drop_imported:
                self.drop_data(table_name=parcel_table, schema=schema)
                self.drop_data(table_name=swis_table, schema=schema)
                self.drop_data(table_name=parcel_parid_table, schema=schema)
                self.drop_data(table_name=res_bldg_table, schema=schema)

            # commit session changes
            db.session.commit()

    def update_parcel(self):
        """
        Update parcel fields
        """
        import time
        start = time.time()

        db.session.execute(queries.update_parcel_fields_query)
        print(f'Updated parcel fields in time: {time.time() - start} seconds')

    def create_parcel_parid(self, table_name, schema):
        """
        Create 'suffolk_parcel_parid' table, construct and insert required data
        """
        df = pd.DataFrame(columns=['muni_code', 'parcel_id', 'par_id', 'sec', 'block', 'lot', 'dist_cd', 'print_key'],
                          dtype=str)
        # create empty 'suffolk_parcel_parid' table
        self.import_data(df, table_name=table_name, schema=schema)

        # insert data
        for q in queries.parcel_parid_insert_queries:
            db.session.execute(q)

        print("Created 'suffolk_parcel_parid' table")

    def parse_parcel(self, df):
        """
        Parse parcel fields
        """

        # parse columns
        df['loc_st_nbr'] = df['loc_st_nbr'].str.strip()
        df['loc_st_name'] = df['loc_st_name'].str.strip()
        df['loc_mail_st_suff'] = df['loc_mail_st_suff'].str.strip()

        df['state'] = 'NY'
        df['loc_zip'] = df['loc_zip'].apply(lambda x: x if x.isdigit() else None)

        df['unit_name'] = df['loc_unit_name'].str.strip()
        df['unit_number'] = df['loc_unit_nbr'].str.strip()

        df['address_line_1'] = ((df['loc_st_nbr'] + ' ' + df['loc_st_name']).str.strip() + ' ' +
                                df['loc_mail_st_suff']).str.strip()
        df['address_line_2'] = (df['unit_name'] + ' ' + df['unit_number']).str.strip()

        df['address_line_1'] = df['address_line_1'].apply(capitalize_address)
        df['address_line_2'] = df['address_line_2'].apply(capitalize_address)

        df['loc_st_nbr'] = df['loc_st_nbr'].apply(capitalize_address)
        df['loc_st_name'] = df['loc_st_name'].apply(capitalize_address)

        print('Parse parcel.txt')
        return df

    def parse_res_bldg(self, df):
        """
        Parse 'res_bldg' fields
        """
        # parse 'bldg_style' column and store it in new df column 'property_style'
        df['property_style'] = df['bldg_style'].apply(self.parse_res_bldg_style)
        print('Parse res_bldg.txt')
        return df

    def parse_res_bldg_style(self, bldg_style):
        if pd.isna(bldg_style):
            return ''
        elif bldg_style.isnumeric():
            return PROPERTY_STYLE_MAP.get(County.SUFFOLK).get(int(bldg_style), '')
        else:
            return ''

    def update_resbld(self):
        import time
        start = time.time()

        db.session.execute(queries.update_res_bldg_inventories_query)
        print(f'Updated inventory fields in {time.time() - start} seconds')

    @staticmethod
    def read_parcel(file_path):
        """
        Read parcel.txt into dataframe
        """
        parcel = pd.read_csv(
            file_path,
            usecols=[
                'parcel_id',
                'block',
                'section',
                'sub_sec',
                'lot',
                'sub_lot',
                'swis_co',
                'swis_muni',
                'print_key',
                'muni_code',
                'swis_vlg',
                'suffix',
                'grid_east',
                'grid_north',
                'loc_st_nbr',
                'loc_st_name',
                'loc_mail_st_suff',
                'loc_muni_name',
                'loc_unit_name',
                'loc_unit_nbr',
                'loc_zip',
                'owner_id'
            ],
            engine='python',
            delimiter=r"\t",
            dtype='str'
        )
        parcel = parcel.replace({pd.np.nan: ''})
        print(f"Read '{file_path.name}' ")
        return parcel

    @staticmethod
    def read_swis(file_path):
        """
        Read swis data from 'Suffolk Swis.xlsx' file to dataframe
        """
        df = pd.read_excel(
            file_path,
            usecols="A:K",
            dtype=str
        )
        df = df.replace({pd.np.nan: ''})
        df['town_nm'] = df['town_nm'].apply(capitalize_address)
        print(f"Read '{file_path.name}' ")
        return df

    @staticmethod
    def read_res_bldg(file_path):
        """
        Read res_bldg.txt file to dataframe
        """
        df = pd.read_csv(
            file_path,
            dtype='str',
            engine='python',
            delimiter=r"\t",
        )
        print(f"Read '{file_path.name}' ")
        return df
