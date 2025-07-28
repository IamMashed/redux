from app.data_import.processor import PersistDataMixin
from my_logger import logger
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine

from app import db
from app.data_import.florida import commit_property, map_row, execute_task, GISProcessor, \
    FloridaPropertyProcessor, FileProcessor, PoolProcessor
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.database.models.property import MiamidadePropertySchema
from app.utils.comp_utils import is_whitelisted
from app.utils.constants import County, SqftInAcre
from app.utils.fix_address import capitalize_address
from config import SQLALCHEMY_DATABASE_URI

MIAMI_DADE_PATIO_TYPES = {
    0: 'NONE',
    1: 'Patio - Concrete Slab',
    2: 'Patio - Brick, Tile, Flagstone',
    3: 'Patio - Terrazzo, Pebble',
    4: 'Patio - Concrete Slab w/Roof Aluminum or Fiber',
    5: 'Patio - Screened over Concrete Slab',
    6: 'Patio - Wood Deck',
    7: 'Patio - Marble',
    8: 'Patio - Concrete stamped or stained',
    9: 'Patio - Exotic hardwood, Ipe, Tigerwood, Mahagony',
    10: 'ATTACHED COVERED PATIO',
    11: 'ALUM COVERED PATIO',
    12: 'PATIO ENCLOSURE',

}

MIAMI_DADE_CONDITION_TYPES = {
    0: 'NONE',
    1: 'Cent A/C - Comm (Aprox 300 sqft/Ton)',
    2: 'Chill Water A/C (Aprox 300 sqft/Ton)',
    3: 'Central A/C (Aprox 400 sqft/Ton)',
}

MIAMI_DADE_PAVING_TYPES = {
    0: 'NONE',
    1: 'Paving - Asphalt',
    2: 'Paving - Concrete',
}


class MiamidadePropertyProcessor(FloridaPropertyProcessor):
    col_names = [
        'folio', 'property_address', 'property_city', 'property_zip', 'year', 'land', 'bldg', 'total', 'assessed',
        'wvdb', 'hex', 'gpar', 'county_2nd_hex', 'county_senior', 'county_longtermsenior', 'county_other_exempt',
        'county_taxable', 'city_2nd_hex', 'city_senior', 'city_longtermsenior', 'city_other_exempt', 'city_taxable',
        'millcode', 'land_use', 'zoning', 'owner1', 'owner2', 'mailing_address', 'mailing_city', 'mailing_state',
        'mailing_zip', 'mailing_country', 'legal1', 'legal2', 'legal3', 'legal4', 'legal5', 'legal6', 'adjustedsqft',
        'lotsize', 'bed', 'bath', 'stories', 'units', 'yearbuilt', 'effectiveyearbuilt', 'sale_type_1', 'sale_qual_1',
        'sale_date_1', 'sale_amt_1', 'sale_type_2', 'sale_qual_2', 'sale_date_2', 'sale_amt_2', 'sale_type_3',
        'sale_qual_3', 'sale_date_3', 'sale_amt_3', 'xf1', 'xf2', 'xf3', 'livingsqft', 'actualsqft'
    ]

    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(MiamidadePropertyProcessor, self).__init__(
            provider_name='miamidade',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def process_input_file(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, skiprows=4, low_memory=False, names=self.col_names)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df.fillna('', inplace=True)

        execute_task(self.process_row, iterator=df.iterrows(), total=len(df), desc=f'process {self.file_name}')

    def parse_street(self, row):
        address = row.property_address.strip()

        if self._valid_address(address):
            return address[len(address.split(' ')[0]):]

        return None

    @staticmethod
    def _valid_address(address):
        splits = address.split(' ')

        if len(splits) > 1:
            if splits[0].isnumeric():
                return True
        return False

    def parse_number(self, row):
        address = row.property_address.strip()
        if self._valid_address(address):
            return str(address.split(' ')[0])

        return None

    @staticmethod
    def parse_patio_type(row):
        for xf in [row.xf1, row.xf2, row.xf3]:
            if xf != '':
                # TODO: save first found patio for now, need client response
                keys = [k for k, v in MIAMI_DADE_PATIO_TYPES.items() if v == xf.strip()]
                if keys:
                    return keys[0]
        return 0

    @staticmethod
    def parse_pool(row):
        reg = 'pool'
        if reg in row.xf1.lower() or reg in row.xf2.lower() or reg in row.xf3.lower():
            return True
        return False

    @staticmethod
    def parse_condition_type(row):
        for xf in [row.xf1, row.xf2, row.xf3]:
            if xf != '':
                # TODO: save first found condition type, need client response
                keys = [k for k, v in MIAMI_DADE_CONDITION_TYPES.items() if v == xf.strip()]
                if keys:
                    return str(keys[0])
        return 0

    @staticmethod
    def parse_paving_type(row):
        for xf in [row.xf1, row.xf2, row.xf3]:
            if xf != '':
                # TODO: save first found paving type, need client response
                keys = [k for k, v in MIAMI_DADE_PAVING_TYPES.items() if v == xf.strip()]
                if keys:
                    return keys[0]
        return 0

    @staticmethod
    def parse_property_class(row):
        try:
            return int(row.land_use.strip().split('-')[0])
        except ValueError:
            return None

    @staticmethod
    def parse_living_sqft(value):
        if value is None or value == '':
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def parse_waterfront(row):
        reg = 'waterfront'
        if reg in row.legal1.lower() or reg in row.legal2.lower() or reg in row.legal4.lower():
            return True
        return False

    @staticmethod
    def parse_zip(row):
        zip_code = row.property_zip
        if zip_code is None or zip_code == "":
            return None
        try:
            return int(zip_code[0:5])
        except ValueError:
            return None

    def process_row(self, row):
        parsed_row = self.parse_row(row)

        property_map, property_errors = map_row(parsed_row, MiamidadePropertySchema)
        property_map['is_residential'] = is_whitelisted(**property_map)

        # export to db
        if self.persist:
            commit_property(property_map, property_errors)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / self.file_name
            append_row_to_csv(property_map, output_path.as_posix())

    def parse_row(self, row) -> dict:
        parsed_row = dict()

        parsed_row['apn'] = row.folio
        parsed_row['county'] = self.provider_name
        parsed_row['section'] = parsed_row['apn'][0:2]
        parsed_row['block'] = parsed_row['apn'][8:10]
        parsed_row['lot'] = parsed_row['apn'][10:12]

        parsed_row['address'] = capitalize_address(row.property_address)
        parsed_row['street'] = capitalize_address(self.parse_street(row))
        parsed_row['number'] = self.parse_number(row)
        parsed_row['zip'] = self.parse_zip(row)
        parsed_row['city'] = capitalize_address(row.property_city)
        parsed_row['is_condo'] = True if 'condo' in row.land_use.lower() else False

        parsed_row['property_class'] = self.parse_property_class(row)
        parsed_row['age'] = row.yearbuilt
        parsed_row['gla_sqft'] = self.parse_living_sqft(row.livingsqft)
        parsed_row['waterfront'] = self.parse_waterfront(row)
        parsed_row['full_baths'] = row.bath
        parsed_row['bedrooms'] = row.bed
        parsed_row['patio_type'] = self.parse_patio_type(row)
        parsed_row['is_pool'] = self.parse_pool(row)
        parsed_row['condition_type'] = self.parse_condition_type(row)
        parsed_row['paving_type'] = self.parse_paving_type(row)
        parsed_row['lot_size_sqft'] = row.lotsize

        # normalize lotsize to acres
        parsed_row['lot_size'] = row.lotsize / SqftInAcre
        parsed_row['lot_size'] = parsed_row['lot_size'].round(decimals=4)

        return parsed_row


class MiamidadeGISProcessor(GISProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(MiamidadeGISProcessor, self).__init__(
            provider_name='miamidade',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def process_gis(self):
        gis_path = self.input_dir() / self.file_name
        df = pd.read_csv(
            gis_path,
            low_memory=False,
            dtype={'FOLIO': str},
            usecols=['FOLIO', 'X_COORD', 'Y_COORD']
        )

        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X_COORD, df.Y_COORD))
        gdf.crs = {'init': 'epsg:2236'}

        # save geometry as x,y points
        gdf['xy_geometry'] = gdf['geometry']

        # convert to latitude/longitude coordinate reference system
        gdf.to_crs(epsg=4326, inplace=True)
        gdf.rename(columns={'geometry': 'lat_long_geometry'}, inplace=True)

        execute_task(self.process_row, iterator=gdf.iterrows(), total=len(gdf), desc=f'process {self.file_name}')

    def parse_row(self, row):
        # parsed_row = super(MiamidadeGISProcessor, self).parse_row(row)

        parsed_row = dict()
        parsed_row['apn'] = row.FOLIO
        parsed_row['county'] = self.provider_name
        parsed_row.update(self.parse_label_coordinates(row))

        return parsed_row


class MiamidadeLandTypeCodeProcessor(FileProcessor):
    def __init__(self, persist, csv):
        super(MiamidadeLandTypeCodeProcessor, self).__init__(
            provider_name=County.MIAMIDADE,
            table='property',
            persist=persist,
            to_file=csv
        )
        self._file_name = 'Public Land Extract.csv'

    def process_file(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, skiprows=3, low_memory=False)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df.fillna('', inplace=True)

        df = df[['Folio', 'UseCode']]
        df.rename(columns={'Folio': "apn", "UseCode": "land_type_code"}, inplace=True)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / 'land_type_codes.csv', index=True, index_label='id')

        if self.persist:
            self._persist_land_type_codes(df)

    def _persist_land_type_codes(self, df):
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URI)
            with engine.connect() as conn, conn.begin():
                df.to_sql('miamidade_land_type_codes', conn, "public", if_exists="replace", index_label='id')
                print("Created temporary 'miamidade_land_type_codes' table")

            statement = '''
                        UPDATE property
                        SET land_type_code = miamidade_land_type_codes.land_type_code
                        FROM miamidade_land_type_codes
                        WHERE property.apn = miamidade_land_type_codes.apn
                        AND property.county = 'miamidade';
                        '''

            print('updating property table')
            db.session.execute(statement)
            print("property 'land_type_code' updated")

            drop_tmp_table_stmt = '''DROP TABLE miamidade_land_type_codes;'''
            db.session.execute(drop_tmp_table_stmt)
            db.session.commit()
            print('delete temporary table')

        except Exception as e:
            print(e.args)


class MiamidadeInventoryUpdateProcessor(FileProcessor, PersistDataMixin):
    def __init__(self, persist, csv, file_name, drop_imported):
        super(MiamidadeInventoryUpdateProcessor, self).__init__(
            provider_name='miamidade',
            table='property',
            persist=persist,
            to_file=csv
        )
        self.drop_imported = drop_imported
        self._file_name = file_name

    def process_file(self, **kwargs):
        df = self.prepare_data(from_file=kwargs.get('from_file'), file_name=kwargs.get('file_name'))
        df = self.parse_data(df)
        if self.to_file:
            df.to_csv(self.output_dir() / f'{self.provider_name}_inventory.csv', index=True, index_label='id')

        if self.persist:
            self.persist_data(df, **kwargs)

    def persist_data(self, df, create_table: bool = True, update_data: bool = True):
        table_name = f'{self.provider_name}_inventory'
        schema = 'data_source'

        if create_table:
            self.import_data(df, table_name, schema=schema)

        if update_data:
            self._create_property_id(table_name, schema)
            self.update_inventory(table_name, schema)

        if self.drop_imported:
            self.drop_data(table_name, schema=schema)

        # persist database changes
        db.session.commit()

    def update_inventory(self, table_name, schema):
        db.session.execute(
            f'''
            update public.property
            set
            lot_size = ROUND(mi.lot_size::numeric, 4),
            gla_sqft = mi.gla_sqft,
            bedrooms = mi.bedrooms,
            full_baths = mi.full_baths,
            patio_type = mi.patio_type,
            waterfront = mi.waterfront,
            condition = mi.condition,
            year = mi.year,
            paving_type = mi.paving_type

            from {schema}.{table_name} as mi
            where public.property.id = mi.property_id
            and mi.property_id is not null;
            '''
        )
        print('updated inventory')

    def _create_property_id(self, table_name, schema):
        db.session.execute(f'ALTER TABLE {schema}.{table_name} ADD COLUMN property_id int;')
        print("Added property_id")
        db.session.execute(
            f'''
            UPDATE {schema}.{table_name}
            SET property_id = property.id
            FROM property
            WHERE property.apn = {schema}.{table_name}.apn
            AND property.county = '{self.provider_name}'
            '''
        )
        print("Updated property_id")

    def parse_data(self, df):
        # normalize lot size
        df['lotsize'] = df['lotsize'] / 43560
        df.rename(
            columns={
                'folio': "apn",
                "lotsize": "lot_size",
                "bed": "bedrooms",
                "bath": "full_baths"
            },
            inplace=True
        )
        df[['xf1', 'xf2', 'xf3', 'legal1', 'legal2', 'legal4']] = df[
            ['xf1', 'xf2', 'xf3', 'legal1', 'legal2', 'legal4']
        ].fillna('')

        # set defaults
        df['gla_sqft'] = df['livingsqft'].apply(MiamidadePropertyProcessor.parse_living_sqft)

        df['gla_sqft'] = df['gla_sqft'].astype('float')

        df['patio_type'] = df.apply(MiamidadePropertyProcessor.parse_patio_type, axis=1)
        df['waterfront'] = df.apply(MiamidadePropertyProcessor.parse_waterfront, axis=1)
        # df['pool'] = df.apply(MiamidadePropertyProcessor.parse_pool, axis=1)
        df['condition'] = df.apply(MiamidadePropertyProcessor.parse_condition_type, axis=1)
        df['paving_type'] = df.apply(MiamidadePropertyProcessor.parse_paving_type, axis=1)
        df['year'] = 2020
        df['new_record'] = False

        # remove legal*,  xf* columns
        df.drop(['legal1', 'legal2', 'legal4', 'xf1', 'xf2', 'xf3'], axis=1, inplace=True)
        print(f"Total data count: {len(df)}")

        return df

    def prepare_data(self, from_file: bool = False, file_name=None):

        if from_file and file_name:
            df = pd.read_csv(self.input_dir() / file_name)
            print(df.dtypes)
            print(df.info())
            df['gla_sqft'] = df['gla_sqft'].fillna('0.00')
            df['gla_sqft'] = df['gla_sqft'].astype('float')

            return df

        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(
            file_path,
            names=MiamidadePropertyProcessor.col_names,
            usecols=[
                'folio', 'lotsize', 'bed', 'bath', 'xf1', 'xf2', 'xf3', 'livingsqft', 'legal1', 'legal2', 'legal4'
            ],
            skiprows=4,
            low_memory=False,
        )

        # delete last row
        df.drop(df.tail(1).index, inplace=True)

        return df


class MiamidadePoolProcessor(PoolProcessor):
    def __init__(self, persist, csv):
        super(MiamidadePoolProcessor, self).__init__(
            county=County.MIAMIDADE,
            persist=persist,
            csv=csv,
            file_name='Public Swimming Pool Extract.csv'
        )

    def process_file(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, skiprows=3, low_memory=False)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df.fillna('', inplace=True)

        df = df[['Folio', 'ShortDescription']]
        print(f"Total data count: {len(df)}")
        df = df[df['ShortDescription'].str.contains("POOL", na=False)]
        print(f"Pool data count: {len(df)}")

        df.rename(columns={'Folio': "apn", "ShortDescription": "description"}, inplace=True)
        df['pool'] = True
        self.output_pool_results(df)


class MiamidadeCondoCodesProcessor(FileProcessor, PersistDataMixin):
    def __init__(self, persist, csv, file_name, drop_imported):
        super(MiamidadeCondoCodesProcessor, self).__init__(
            provider_name=County.MIAMIDADE,
            table='property',
            persist=persist,
            to_file=csv
        )
        self.drop_imported = drop_imported
        self._file_name = file_name

    def prepare_data(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, low_memory=False)
        logger.info('Read data source')

        # remove useless columns to reduce memory usage
        df = df[['Strap', 'CONDO_VIEW', 'StripNumber']]
        df.rename(columns={'Strap': "apn", 'CONDO_VIEW': 'condo_codes', 'StripNumber': 'strip_number'}, inplace=True)

        # remove null records
        # df = df[~df.condo_codes.isna()]
        df = df[~df.apn.isna()]

        # take third from the end as a condo location
        # create condo view location, condo view influence columns
        #  code 'L1BV' --> '1' + 'BV',
        #  code 'LSCR' --> 'S' + 'CR'
        df['condo_view_location'] = df['condo_codes'].str[-3]
        df['condo_view_location'] = df['condo_view_location'].astype(str)

        df['condo_view_influence'] = df['condo_codes'].str[-2:]
        df['condo_view_influence'] = df['condo_view_influence'].astype(str)
        logger.info("Parse from 'condo_codes'")

        df.fillna('', inplace=True)
        df = df.apply(self.parse_strip_number, axis=1)
        logger.info("Parse from 'strip_number'")

        df["condo_view_location"] = df["condo_view_location"].apply(lambda x: 'N/A' if 'nan' in str(x) else x)
        df["condo_view_influence"] = df["condo_view_influence"].apply(lambda x: 'N/A' if 'nan' in str(x) else x)

        return df

    def parse_strip_number(self, row):
        # parse condo view code from strip number only if 'condo_code' is empty and valid 'strip_number' to parse
        strip_number = str(row['strip_number']).strip()
        if len(strip_number) < 3 or not strip_number[-2:].isalpha() or len(row['condo_codes']) >= 3:
            return row

        row['condo_view_location'] = strip_number[-3].upper()
        row['condo_view_influence'] = strip_number[-2:].upper()

        return row

    def process_file(self, **kwargs):
        df = self.prepare_data()

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / f'{self.provider_name}_condo_codes.csv', index=True, index_label='id')
            logger.info(f'Export to: {self.provider_name}_condo_codes.csv')

        if self.persist:
            # to speed up and reduce memory usage, exclude useless columns
            df = df[['apn', 'condo_view_location', 'condo_view_influence']]

            logger.info(f"Total data source length: {len(df)}")
            # df = df[~df["condo_view_location"].str.contains('nan')]
            # logger.info("Filter 'nan' condo_view_location and condo_view_influence")
            logger.info(f"Parsed data source length: {len(df)}")
            self.persist_condo_codes(df, **kwargs)
            db.session.commit()

    def persist_condo_codes(self, df, create_table: bool = True, update_data: bool = True):
        table_name = f'{self.provider_name}_condo_codes'
        schema = 'data_source'

        if create_table:
            self.import_data(df, table_name, schema=schema)

        if update_data:
            db.session.execute(
                f'''
                update public.property
                set
                condo_view_location = mcc.condo_view_location,
                condo_view_influence = mcc.condo_view_influence
                from {schema}.{table_name} as mcc
                where public.property.apn = mcc.apn;
                '''
            )
            logger.info('Update miamidade condo codes in property table')

        if self.drop_imported:
            self.drop_data(table_name=table_name, schema=schema)
