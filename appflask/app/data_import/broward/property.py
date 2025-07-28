import math

import pandas as pd

from app import db
from app.data_import.florida import GISProcessor, execute_task, map_row, \
    read_shp, FloridaPropertyProcessor, commit_property, PoolProcessor, FileProcessor
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.data_import.processor import PersistDataMixin
from app.database.models.property import BrowardPropertySchema
# Then export .dbf to .csv file.
# IMPORTANT: GIS dbf file for Broward has invalid format in the first column.
# Exclude columns: ['CONFIDENCE', 'NOTES', 'CLASSIFICA'], we don't use them
from app.utils.comp_utils import is_whitelisted
from app.utils.constants import County, SqftInAcre
from app.utils.fix_address import capitalize_address
# You first need to install mdb-tools:
# sudo apt install mdbtools
# To list the tables do this:
# mdb-tables database.mbd
# Convert .mdb to desired table
# mdb-export database.mdb table > table.csv
# To prepare GIS input file to be ready for the processing, install DBF Viewer 2000.

BROWARD_CITY_ABBR = {
    'BC': 'UNINCORPORATED',
    'CK': 'COCONUT CREEK',
    'CS': 'CORAL SPRINGS',
    'CY': 'COOPER CITY',
    'DB': 'DEERFIELD BEACH',
    'DN': 'DANIA BEACH',
    'DV': 'DAVIE',
    'FL': 'FORT LAUDERDALE',
    'HA': 'HALLANDALE BEACH',
    'HB': 'HILLSBORO BEACH',
    'HW': 'HOLLYWOOD',
    'LH': 'LAUDERHILL',
    'LL': 'LAUDERDALE LAKES',
    'LP': 'LIGHTHOUSE POINT',
    'LS': 'LAUD BY THE SEA',
    'LZ': 'LAZY LAKE',
    'MG': 'MARGATE',
    'MM': 'MIRAMAR',
    'NL': 'NORTH LAUDERDALE',
    'OP': 'OAKLAND PARK',
    'PA': 'PARKLAND',
    'PB': 'POMPANO BEACH',
    'PI': 'PEMBROKE PINES',
    'PK': 'PEMBROKE PARK',
    'PL': 'PLANTATION',
    'SL': 'SEA RANCH LAKES',
    'SU': 'SUNRISE',
    'SW': 'SOUTHWEST RANCHES',
    'TM': 'TAMARAC',
    'WM': 'WILTON MANORS',
    'WP': 'WEST PARK',
    'WS': 'WESTON'
}


class BrowardPropertyProcessor(FloridaPropertyProcessor):
    """
    Broward property file processor
    """

    stamp_rates_data = {
        'start_date': ("01/01/1931", "01/07/1957", "01/07/1963", "01/10/1979",
                       "01/07/1981", "01/07/1985", "01/07/1987", "01/06/1991",
                       "01/08/1992"),

        'end_date': ("30/06/1957", "30/06/1963", "30/09/1979", "30/06/1981",
                     "30/06/1985", "30/06/1987", "31/05/1991", "31/07/1992",
                     None),
        'stamp_rate': (0.0010, 0.0020, 0.0030, 0.0040, 0.0045, 0.0050, 0.0055,
                       0.0060, 0.0070),
    }

    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(BrowardPropertyProcessor, self).__init__(
            provider_name='broward',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name
        self._stamp_rates = pd.DataFrame(self.stamp_rates_data)

    def get_stamp_rate(self, sale_date) -> float:
        """
        Get stamp rate according to documentation rules.
        Stamp rate depends on sale_date and predefined in 'stamp_rates.csv'.

        :param sale_date: The Sale Date
        :return: Stamp Rate
        """

        sale_date = pd.to_datetime(sale_date, dayfirst=False)
        for i in range(len(self._stamp_rates)):
            row = self._stamp_rates.iloc[i]
            start_date = row['start_date']
            end_date = row['end_date']

            if sale_date >= pd.to_datetime(start_date):
                if end_date is None:
                    return row['stamp_rate']
                elif sale_date <= pd.to_datetime(end_date):
                    return row['stamp_rate']

    def get_sale_price(self, row):
        """ Get sale price or property """

        # STAMP_AMOUNT_1
        stamp_amount = row.STAMP_AMOUNT_1

        # SALE_DATE_1
        sale_date = row.SALE_DATE_1

        if sale_date == '' or stamp_amount == '':
            return None

        stamp_rate = self.get_stamp_rate(sale_date)

        if stamp_rate is None:
            return None

        return float(stamp_amount) / stamp_rate

    @staticmethod
    def parse_property_class_type(row):
        val = row.USE_TYPE
        if val == '' or val is None:
            return None
        try:
            class_type = int(float(val))
            return class_type
        except ValueError:
            return None

    @staticmethod
    def parse_property_age(row):
        val = row.ACTUAL_YEAR_BUILT
        try:
            year = int(float(val))
            return None if year == 0 else year
        except ValueError:
            return None

    @staticmethod
    def parse_waterfront(row):
        value = row.LAND_TAG
        if value == '':
            return None
        try:
            value = int(value)
            if value in range(1, 17) or value in [24, 25, 26, 28, 62, 63, 64] or value in range(77, 87):
                return True
            else:
                return False
        except ValueError:
            return None

    @staticmethod
    def parse_gla_sqft(row):
        value = row.BLDG_ADJ_SQ_FOOTAGE
        if value == '':
            return None
        try:
            value = float(value)
        except ValueError:
            return None
        return value

    @staticmethod
    def parse_under_air_gla_sqft(row):
        value = row.BLDG_UNDER_AIR_SQ_FOOTAGE
        if value == '':
            return None
        try:
            value = float(value)
        except ValueError:
            return None
        return value

    def parse_price_per_sqft(self, row, digits: int = 4):
        sale_price = self.get_sale_price(row)

        if (sale_price is None) or sale_price == 0:
            return None
        else:
            gla_sqft = self.parse_gla_sqft(row)

            if gla_sqft is None:
                return None

            return round(float(gla_sqft) / sale_price, ndigits=digits)

    @staticmethod
    def parse_full_baths(row):
        val = str(row.BATHS)
        try:
            return int(math.modf(float(val))[1])
        except ValueError:
            return None

    @staticmethod
    def parse_bedrooms(row):
        value = row.BEDS
        try:
            return int(float(value))
        except ValueError:
            return None

    @staticmethod
    def parse_half_baths(row):
        val = str(row.BATHS)
        try:
            rest = math.modf(float(val))[0]
            return 1 if rest > 0 else 0
        except ValueError:
            return None

    @staticmethod
    def parse_zip(row):
        try:
            return int(row.ZIP)
        except ValueError:
            return 0

    @staticmethod
    def parse_street_number(row):
        try:
            return str(row.SITUS_STREET_NUMBER)
        except ValueError:
            return None

    @staticmethod
    def parse_city(row):
        if row.SITUS_CITY == '' or row.SITUS_CITY is None:
            return 'None'
        try:
            return BROWARD_CITY_ABBR[row.SITUS_CITY]
        except ValueError:
            return 'None'

    @staticmethod
    def parse_address(row):

        # address example
        # 434 - 436 S DIXIE HIGHWAY E POMPANO BEACH, 33060

        st_num = row.SITUS_STREET_NUMBER
        st_num_end = row.SITUS_STREET_NUMBER_END
        st_dir = row.SITUS_STREET_DIRECTION
        st_name = row.SITUS_STREET_NAME
        st_type = row.SITUS_STREET_TYPE
        st_post_dir = row.SITUS_STREET_POST_DIR
        st_units = row.SITUS_UNIT_NUMBER
        st_city = BROWARD_CITY_ABBR.get(row.SITUS_CITY, '')
        st_zip = row.SITUS_ZIP_CODE

        pre_addr = ""
        if str(st_num) != '':
            if str(st_num_end) != '':
                pre_addr = "{} - {}".format(st_num, st_num_end)
            else:
                pre_addr = str(st_num)

        units = ""
        if st_units != "":
            units = "#" + st_units

        post_addr = "{} {} {} {} {} {}, {}".format(st_dir, st_name, st_type, st_post_dir, units, st_city, st_zip)
        address = "{} {}".format(pre_addr, post_addr)

        return address

    def process_input_file(self):
        """ Process input file from data source """
        file_path = self.input_dir() / self.file_name

        # read only needed cols to reduce memory usage
        df = pd.read_csv(
            file_path,
            usecols=[
                'FOLIO_NUMBER', 'SITUS_STREET_NAME', 'SITUS_STREET_NUMBER', 'SITUS_STREET_DIRECTION',
                'SITUS_STREET_TYPE', 'SITUS_STREET_POST_DIR', 'SITUS_STREET_NUMBER_END', 'SITUS_ZIP_CODE',
                'SITUS_UNIT_NUMBER', 'STATE', 'ZIP', 'LAND_TAG', 'BLDG_CCLASS', 'ACTUAL_YEAR_BUILT',
                'BLDG_ADJ_SQ_FOOTAGE', 'BATHS', 'BEDS', 'USE_CODE', 'USE_TYPE', 'STAMP_AMOUNT_1', 'SALE_DATE_1',
                'BLDG_TOT_SQ_FOOTAGE', 'MILLAGE_CODE', 'SITUS_CITY', 'NAME_LINE_1', 'NAME_LINE_2', 'ADDRESS_LINE_1',
                'CITY', 'BLDG_UNDER_AIR_SQ_FOOTAGE', 'LAND_CALC_FACT_1'
            ],
            low_memory=False,
        )

        # normalize lot size
        df['BLDG_TOT_SQ_FOOTAGE'] = df['BLDG_TOT_SQ_FOOTAGE'] / SqftInAcre
        df['BLDG_TOT_SQ_FOOTAGE'] = df['BLDG_TOT_SQ_FOOTAGE'].round(decimals=4)

        df.fillna('', inplace=True)
        df = df.astype(str)

        execute_task(self.process_row, iterator=df.iterrows(), total=len(df), desc=f'process {self.file_name}')

    def process_row(self, row):
        parsed_row = self.parse_row(row)

        # map data with marshmallow schema
        property_map, property_errors = map_row(parsed_row, BrowardPropertySchema)
        property_map['is_residential'] = is_whitelisted(**property_map)

        if property_errors:
            print(property_errors)

        # export to db
        if self.persist:
            # commit property
            commit_property(property_map, property_errors)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / self.file_name
            # owner_path = self.output_dir() / ('OWNER_' + self.file_name)

            append_row_to_csv(property_map, output_path.as_posix())
            # append_row_to_csv(owner_map, owner_path.as_posix())

    def parse_row(self, row):
        parsed_row = dict()

        parsed_row['apn'] = row.FOLIO_NUMBER
        parsed_row['county'] = self.provider_name
        parsed_row['section'] = parsed_row.get('apn')[4:6]
        parsed_row['block'] = parsed_row.get('apn')[6:8]
        parsed_row['lot'] = parsed_row.get('apn')[8:11]
        parsed_row['address'] = capitalize_address(self.parse_address(row))
        parsed_row['street'] = capitalize_address(row.SITUS_STREET_NAME)
        parsed_row['number'] = self.parse_street_number(row)
        parsed_row['city'] = capitalize_address(self.parse_city(row))
        parsed_row['state'] = row.STATE
        parsed_row['zip'] = self.parse_zip(row)

        parsed_row['is_condo'] = True if parsed_row.get('apn')[6].isalpha() else False
        parsed_row['is_waterfront'] = self.parse_waterfront(row)
        parsed_row['property_class'] = row.USE_CODE
        parsed_row['property_class_type'] = self.parse_property_class_type(row)

        parsed_row['age'] = self.parse_property_age(row)
        parsed_row['gla_sqft'] = self.parse_gla_sqft(row)
        parsed_row['under_air_gla_sqft'] = self.parse_under_air_gla_sqft(row)

        parsed_row['full_baths'] = self.parse_full_baths(row)
        parsed_row['half_baths'] = self.parse_half_baths(row)
        parsed_row['bedrooms'] = self.parse_bedrooms(row)

        parsed_row['property_style'] = None
        parsed_row['price_per_sqft'] = self.parse_price_per_sqft(row)
        parsed_row['lot_size'] = row.LAND_CALC_FACT_1
        parsed_row['lot_size_sqft'] = row.LAND_CALC_FACT_1

        # convert lot_size to acres
        parsed_row['lot_size'] = parsed_row['lot_size'] / SqftInAcre
        parsed_row['lot_size'] = parsed_row['lot_size'].round(decimals=4)

        return parsed_row


class BrowardGISProcessor(GISProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(BrowardGISProcessor, self).__init__(
            provider_name='broward',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def process_gis(self):
        gis_path = self.input_dir() / self.file_name
        gdf = read_shp('zip://' + gis_path.as_posix())

        execute_task(self.process_row, iterator=gdf.iterrows(), total=len(gdf), desc=f'process {self.file_name}')

    def parse_row(self, row):
        parsed_row = dict()
        parsed_row['apn'] = row.FOLIO
        parsed_row['county'] = self.provider_name
        parsed_row.update(self.parse_label_coordinates(row))

        return parsed_row


class BrowardPoolProcessor(PoolProcessor):
    def __init__(self, persist, csv):
        super(BrowardPoolProcessor, self).__init__(
            county=County.BROWARD,
            persist=persist,
            csv=csv,
            file_name='BCPA_POOL.csv'
        )

    def process_file(self):
        """
        Integrate Broward pool data
        """

        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, low_memory=False, dtype=str)
        df.fillna('', inplace=True)

        df = df[['FOLIO_NUMBER', 'EXTRA_FEATURES']]
        print(f"Total data count: {len(df)}")
        df = df[df['EXTRA_FEATURES'].str.contains("POOL", na=False)]
        print(f"Pool data count: {len(df)}")

        # rename columns to be understandable
        df.rename(columns={'FOLIO_NUMBER': "apn", "EXTRA_FEATURES": "description"}, inplace=True)

        # all records in dataframe has pool
        df['pool'] = True
        self.output_pool_results(df)


class BrowardCondosProcessor(FileProcessor, PersistDataMixin):
    def __init__(self, persist, csv, file_name, drop_imported=False):
        super(BrowardCondosProcessor, self).__init__(
            provider_name=County.BROWARD,
            table='property',
            persist=persist,
            to_file=csv
        )
        self.drop_imported = drop_imported
        self._file_name = file_name

    def read_data(self):
        """
        Read data to be processed
        """
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_excel(
            file_path,
            usecols="A:D",
            dtype=str
        )

        print(f"Read data from file: '{self.file_name}'")
        return df

    def prepare_data(self):
        """
        Prepare data before processing
        """
        df = self.read_data()
        df['FLOOR'] = df['FLOOR'].apply(lambda x: 'N/A' if 'nan' in str(x) or str(x) == '' else x)
        df['LOCATION'] = df['LOCATION'].apply(lambda x: 'N/A' if 'nan' in str(x) or str(x) == '' else x)
        df['VIEWS'] = df['VIEWS'].apply(lambda x: 'N/A' if 'nan' in str(x) or str(x) == '' else x)
        print(df.columns)
        print(df.info())
        return df

    def persist_condo_codes(self, table, schema):
        query = f'''
            update public.property p
            set (condo_view_location, condo_view_influence, condo_view_floor)=
                (
                    bcc."LOCATION",
                    bcc."VIEWS",
                    bcc."FLOOR"
                )
            from {schema}.{table} bcc
            where p.apn = bcc."FOLIO"
        '''

        db.session.execute(query)
        print(f"Updated condo codes for the '{self.provider_name}' county")

    def process_file(self):
        import time
        start = time.time()
        df = self.prepare_data()
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / f'{self.file_name[:-5]}.csv', index=False)

        if self.persist:
            try:
                table_name = f'{self.provider_name}_condo_codes'
                self.import_data(df, table_name, schema='data_source')
                self.persist_condo_codes(table=table_name, schema='data_source')
                if self.drop_imported:
                    self.drop_data(table_name, schema='data_source')
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e.args)
            finally:
                db.session.close()

        print(f'Total processing time: {time.time() - start} seconds')
