import concurrent.futures
import time

import click
import geopandas as gpd
import pandas as pd
from marshmallow import EXCLUDE, ValidationError
from sqlalchemy import create_engine

from app import db
from app.data_import.florida import GISProcessor, execute_task
from app.database.models.property import Property, NassauPropertySchema, PropertyValidation
from app.utils.comp_utils import is_whitelisted
from app.utils.fix_address import capitalize_address
from config import DATA_IMPORT, MAX_WORKER_COUNT, SQLALCHEMY_DATABASE_URI


def rename_duplicates(old):
    """
    Here is a list containing duplicates:
    l1 = ['a', 'b', 'c', 'a', 'a', 'b']

    Here is the desired result:
    l1 = ['a', 'b', 'c', 'a_1', 'a_2', 'b_1']
    """
    seen = {}
    for x in old:
        if x in seen:
            seen[x] += 1
            yield f"{x}_{seen[x]}"
        else:
            seen[x] = 0
            yield x


def parse_row(row):
    """
    Remove first and last character in each cell
    For residential we removing '@'
    For commercial we removing '~'
    """
    return [x[1:-1] for x in row.split(',')]


def commit(property_map, errors):
    apn = property_map['apn']
    county = property_map['county']

    error_at_update = Property.insert(property_map)

    if error_at_update:
        errors['database_operation'] = error_at_update

    # if any errors during validation, store them
    # in the database PropertyValidation table
    if errors and property_map:
        PropertyValidation.update_if_exists(apn, county, errors)
        print(f'the errors are {errors}')
    db.session.commit()


nassau_property_schema = NassauPropertySchema(unknown=EXCLUDE)


def map_row(dict_keys, row):
    """
    Helper method to map input file rows to the Property
    Schema.
    :param dict_keys: first row of input file.
    i.e column names
    :param row: input file rows
    :return: Property mapped dict
    """
    # create structure with dict_keys of the first row
    parsed_row = parse_row(row.strip())
    raw_data = dict(zip(dict_keys, parsed_row))
    # raw_data['X_COORD'] = raw_data.pop('XY_COORD')
    # raw_data['Y_COORD'] = raw_data.pop('')
    # validate raw_data with marshmallow Schema
    error_messages = {}
    try:
        property_map = nassau_property_schema.load(raw_data)
        property_map['is_residential'] = is_whitelisted(**property_map)
    except ValidationError as e:
        error_messages = e.messages
        property_map = e.valid_data

    property_map['address'] = capitalize_address(property_map['address'])
    property_map['street'] = capitalize_address(property_map['street'])
    property_map['town'] = capitalize_address(property_map['town'])
    from manage import app
    with app.app_context():
        commit(property_map, error_messages)
    return property_map


def async_process_input(opened_file, dict_keys):
    start = time.time()
    count = 0
    lines = opened_file.readlines()
    with concurrent.futures.ProcessPoolExecutor(MAX_WORKER_COUNT) as executor:
        # Start the load operations and mark each future with its index
        futures = (
            executor.submit(map_row, dict_keys, line)
            for line in lines
        )
        print('tasks submitted')
        with click.progressbar(length=len(lines),
                               label='processing properties') as bar:
            for future in concurrent.futures.as_completed(futures):
                bar.update(1)
                try:
                    _ = future.result() # noqa
                except Exception as exc:
                    print(exc)
                count += 1
    runtime = time.time() - start
    print("took {} seconds or {} rows per second".format(runtime, count / runtime))

    # for line in lines:
    #     map_row(dict_keys, line)


def process_input_file(file_name, csv, persist):
    input_path = DATA_IMPORT / 'src' / 'nassau' / 'property' / file_name
    output_folder = DATA_IMPORT / 'output' / 'nassau' / 'property'
    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / 'residential.csv'
    output_df = pd.DataFrame()

    with open(input_path) as f:
        # create structure with keys of the first row
        first_row = f.readline()
        keys = parse_row(first_row.strip())
        # append count numbers to duplicates
        keys = list(rename_duplicates(keys))

        if csv:
            for i, row in enumerate(f.readlines()):
                r = map_row(keys, row.strip())
                output_df = output_df.append(r, ignore_index=True)
            output_df.to_csv(output_path, index=None)

        if persist:
            async_process_input(f, keys)


class NassauGISProcessor(GISProcessor):
    def __init__(self, persist: bool, to_file: bool):
        super(NassauGISProcessor, self).__init__(
            provider_name='nassau',
            persist=persist,
            to_file=to_file
        )
        self.include_xy = False

    def process_gis(self):
        self._file_name = "nassau_gis.csv"

        # get x,y coordinates from db
        conn = create_engine(SQLALCHEMY_DATABASE_URI)
        df = pd.read_sql(
            "select apn, county, coordinate_x, coordinate_y from property where county='nassau'",
            conn
        )

        # remove records with empty coordinate_x & coordinate_y
        df = df[~df.coordinate_x.isna()]
        df = df[~df.coordinate_y.isna()]

        # create geo dataframe from coordinate_x, coordinate_y points
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.coordinate_x, df.coordinate_y))
        gdf.crs = {'init': 'epsg:6539'}
        gdf['xy_geometry'] = gdf['geometry']

        # convert to latitude/longitude coordinate reference system
        gdf.to_crs({'init': 'epsg:4326'}, inplace=True)
        gdf.rename(columns={'geometry': 'lat_long_geometry'}, inplace=True)

        # update records in database
        execute_task(self.process_row, iterator=gdf.iterrows(), total=len(gdf))

    def parse_row(self, row):
        parsed_row = dict()
        parsed_row['apn'] = row.apn
        parsed_row['county'] = self.provider_name
        parsed_row.update(self.parse_label_coordinates(row))

        return parsed_row
