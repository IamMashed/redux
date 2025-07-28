import json
import geopandas as gpd
from sqlalchemy import create_engine

from app.data_import.florida import FileProcessor, execute_task
from app.database.models import Property
from app.database.models.property import PropertyGis
from app.utils.constants import County
from config import SQLALCHEMY_DATABASE_URI
from shapely_geojson import dumps, Feature
from geoalchemy2.shape import to_shape

from shapely import speedups
speedups.disable()


def convert_wkb_to_geojson(obs_name, wkb_list):
    """
    Helper function to convert wkbelement to geojson
    """
    if not wkb_list:
        return None
    result = []
    for wkb in wkb_list:
        if isinstance(wkb, PropertyGis):
            wkb = wkb.geometry
        feature = Feature(to_shape(wkb))
        gjs = dumps(feature)
        js = json.loads(gjs)
        js['properties']['obs_name'] = obs_name
        result.append(js)
    return result


def get_geometry_type(gdf):
    """
    Get basic geometry type of a GeoDataFrame, and information if the gdf contains Geometry Collections.
    """
    geom_types = list(gdf.geometry.geom_type.unique())
    geom_collection = False

    # Get the basic geometry type
    basic_types = []
    for gt in geom_types:
        if 'Multi' in gt:
            geom_collection = True
            basic_types.append(gt.replace('Multi', ''))
        else:
            basic_types.append(gt)
    geom_types = list(set(basic_types))

    # Check for mixed geometry types
    assert len(geom_types) < 2, "GeoDataFrame contains mixed geometry types, cannot proceed with mixed geometries."
    geom_type = geom_types[0]
    return geom_type, geom_collection


def get_srid_from_crs(gdf):
    """
    Get EPSG code from CRS if available. If not, return -1.
    """
    if gdf.crs is not None:
        try:
            srid = int(gdf.crs['init'].replace('epsg:', ''))
        except ValueError:
            srid = -1
    else:
        srid = -1
    if srid == -1:
        print(
            "Warning: Could not parse coordinate reference system from GeoDataFrame. "
            "Inserting data without defined CRS.")

    return srid


def postgis_to_geojson(con, file_path, table='property_gis', county=None):
    """
    Export postgis geometry to GeoJson file
    :param con: The connection to database
    :param file_path: The output file path
    :param table: The geometry table
    :param county: The county query parameter
    """

    if county:
        sql = "select * from {} where county='{}'".format(table, county)
    else:
        sql = "select * from {}".format(table)

    gdf = gpd.GeoDataFrame.from_postgis(sql, con, geom_col='geometry')
    if gdf.empty:
        print("No records found in '{}' table for the statement: '{}'".format(table, sql))
        return None

    # gdf.to_file(file_path, driver="GeoJSON")
    with open(file_path.as_posix(), 'w') as file:
        file.write(gdf_to_geojson(gdf))
        print("Records {} were exported, file location: {}".format(len(gdf.index), file_path))


def gdf_to_geojson(gdf):
    """
    Convert GeoDataframe to GeoJson
    """
    return gpd.GeoDataFrame.to_json(gdf)


def get_gis_meta(county):
    """
    Get county gis data
    """

    # 'Broward' gis meta data
    if county == County.BROWARD:
        return {
            'column_name': 'FOLIO',
            'file_name': 'BCPA_GIS_POLYGON.zip'
        }

    # 'Nassau' gis meta data
    elif county == County.NASSAU:
        return {
            'column_name': 'SBL',
            'file_name': 'Tax Parcel Data.zip'
        }

    # 'Suffolk' gis meta data
    elif county == County.SUFFOLK:
        return {
            'column_name': 'PARCELID',
            'file_name': 'Land_Use__2016.zip'
        }

    # 'Palm Beach' gis meta data
    elif county == County.PALMBEACH:
        return {
            'column_name': 'PARID',
            'file_name': 'PARCELS.zip'
        }

    # 'Miami Dade' gis meta data
    elif county == County.MIAMIDADE:
        return {
            'column_name': 'FOLIO',
            'file_name': 'Property_Boundary_View.zip'
        }

    else:
        raise ValueError('Invalid county name. No meta data found for the county {}'.format(county))


class GeometryProcessor(FileProcessor):
    """
    Geometry processor class
    """

    def __init__(self, county, persist, to_file):
        super(GeometryProcessor, self).__init__(
            provider_name=county,
            table='gis',
            persist=persist,
            to_file=to_file
        )

        self._meta = get_gis_meta(county)

    def process_geometry(self):
        """
        Process geo spacial file & store into database table
        """
        try:
            if self.persist:
                if not self._meta:
                    raise ValueError(
                        'Warning: No meta data for {} county. Skipped geometry processing.'.format(self.provider_name)
                    )

                self._file_name = self._meta.get('file_name')
                file_path = self.input_dir() / self.file_name

                # create GeoDataframe object
                gdf = self.create_geo_dataframe(file_path)

                # geometry column name
                geom_name = gdf.geometry.name

                # Convert geometries to wkt so that it can be pushed to database
                gdf[geom_name] = gdf[geom_name].apply(lambda geom: geom.wkt)

                # output_path = self.output_dir() / (
                #         f'{self.provider_name}_full' + '.geojson')
                # with open(output_path.as_posix(), 'w') as file:
                #     file.write(gdf_to_geojson(gdf))
                #     print("Records {} were exported, file location: {}".format(len(gdf.index), output_path))

                # multiprocessing store to database
                execute_task(
                    task=self.process_row,
                    iterator=gdf.iterrows(),
                    total=len(gdf),
                    desc=f'process {self.file_name}'
                )

            # read & export from database to .geojson file, ready to upload to Mapbox
            if self.to_file:
                self.output_dir().mkdir(exist_ok=True, parents=True)
                output_path = self.output_dir() / (self.provider_name + '_v2.geojson')

                con = create_engine(SQLALCHEMY_DATABASE_URI)
                postgis_to_geojson(con, file_path=output_path, county=self.provider_name)

        except ValueError as e:
            print(e.args)

    def process_row(self, row):
        """
        Persist row to database table
        """
        errors = dict()
        from manage import app
        with app.app_context():
            try:
                # pop 'apn' & 'county' to get unique property object
                apn = row.get('apn')

                if self.provider_name == County.NASSAU:
                    apn = apn.replace(' ', '  ')
                    apn = apn[:-4] if apn.endswith('0000') else apn
                    row['apn'] = apn
                county = row.get('county')

                prop = Property.query.filter_by(apn=apn, county=county).first()
                if prop:
                    # row['property_id'] = prop.id
                    insert_error = PropertyGis.insert(
                        dict(apn=row.get('apn'),
                             county=county,
                             geometry=row.get('geometry'),
                             property_id=prop.id)
                    )

                    if insert_error:
                        errors['database_operation'] = insert_error

                    if errors and row:
                        print(errors)
                else:
                    # do nothing for now, if no property found
                    print(f'no property with apn {apn} in database. New from gis')
                    # new_prop = Property(
                    #     apn=row.get('apn'),
                    #     origin='gis',
                    #     county=self.provider_name,
                    #     address=row.get('PARCELADDR'),
                    #     print_key=row.get('PRINT_KEY'),
                    #     street=row.get('LOC_STREET'),
                    #     number=row.get('LOC_ST_NBR'),
                    #     property_class=row.get('PROP_CLASS'),
                    #     lot_size=row.get('CALC_ACRES')
                    # )
                    # db.session.add(new_prop)
                    # db.session.commit()
            except Exception as e:
                print(e.args)

    def create_geo_dataframe(self, file_path, to_crs=4326):
        """
        Prepare geo dataframe to store into database
            * read geo spatial file
            * re-project to Mercator
            * convert geometries to wkt
        """

        apn_column_name = self._meta.get('column_name', None)
        if apn_column_name is None:
            raise ValueError('Invalid column name')

        # read geo spacial file to geo dataframe object
        gdf = gpd.GeoDataFrame.from_file('zip://' + file_path.as_posix())

        # remove all columns, except 'apn', 'geometry'
        # gdf = gdf[['geometry', apn_column_name]]

        # rename key column to 'apn', since every county has different key column names
        gdf.rename(columns={apn_column_name: "apn"}, inplace=True)

        # add 'county' column, needed for storing process to identify unique property id by 'apn' & 'county'
        gdf['county'] = self.provider_name
        gdf = gdf[~gdf.geometry.isna()]

        # project to specified projection 'to_crs'
        if to_crs:
            # geo spatial data has been projected to Latitude/Longitude CRS (EPSG:4326)
            # Mapbox require to have data in Mercator projection
            gdf.to_crs(epsg=to_crs, inplace=True)
        else:
            raise ValueError('Invalid crs projection')

        return gdf
