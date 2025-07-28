import json
import urllib.request as request
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine

from app import db
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.routing.services import PropertyService
from config import DATA_IMPORT, SQLALCHEMY_DATABASE_URI
from my_logger import logger

PRIVATE_KEY = "AIzaSyAzIsk4qvLtmne-5yxHs4l08bt2AbWBBP8"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?key=" + PRIVATE_KEY


def parse_address(data):
    # result data
    result_data = {
        "county": None,
        "city": None,
        "country": None,
        "state": None,
        "postal_code": None,
        "postal_code_sufix": None,
        "error_status": None
    }

    if not ('results' in data):
        # No results found
        result_data['error_status'] = 'No Results'
        return result_data

    try:
        address_components = data['results'][0]['address_components']
    except Exception as e:
        print(e)
        logger.info('Incomplete Results')
        result_data['error_status'] = 'Incomplete Results'
        return result_data

    for comp in address_components:

        if 'administrative_area_level_1' in comp['types']:
            result_data['state'] = comp['short_name']
        if 'administrative_area_level_2' in comp['types']:
            result_data['county'] = comp['short_name']
        if 'locality' in comp['types']:
            result_data['city'] = comp['short_name']
        if 'country' in comp['types']:
            result_data['country'] = comp['short_name']
        if 'postal_code' in comp['types']:
            result_data['postal_code'] = comp['short_name']
        if 'postal_code_suffix' in comp['types']:
            result_data['postal_code_sufix'] = comp['short_name']

    return result_data


def process_row(row_data):
    address_line1 = row_data.get("owner_address_line_1") or ""
    address_line2 = row_data.get("owner_address_line_2") or ""
    address_line3 = row_data.get("owner_address_line_3") or ""

    if address_line2 == '' and address_line3 == '':
        city = row_data.get('owner_address_city')
        state = row_data.get('owner_address_state')
        zip_code = row_data.get('owner_address_zip')
        address_line2 = ' '.join([city, state, zip_code])
    complete_url = BASE_URL + "&address=" + \
        quote_plus(address_line1) + "+" + quote_plus(address_line2) + "+" + quote_plus(address_line3)

    response = request.urlopen(complete_url)
    json_data = json.load(response)

    return parse_address(json_data)


def fix_owner_fields():
    """
    Correct owner city, state, zip, country
    """


class FixAddress:

    def _prepare_data(self, file_path):
        df = pd.read_csv(file_path, low_memory=False, dtype=str).fillna('').astype(str)

        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.lower()

        df[['owner_address_line_1', 'owner_address_line_2', 'owner_address_line_3']] = df[
            ['owner_address_line_1', 'owner_address_line_2', 'owner_address_line_3']
        ].fillna('')

        # add new empty columns
        df['owner_google_city'] = ''
        df['owner_google_state'] = ''
        df['owner_google_zip'] = ''
        df['owner_google_zip_sufix'] = ''
        df['owner_google_country'] = ''

        # print(df.info())
        # print(df.columns)

        return df

    def process_file(self, file_name):
        input_dir = DATA_IMPORT / 'src'
        output_dir = DATA_IMPORT / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info('Prepare data frame')
        df = self._prepare_data(file_path=(input_dir / file_name).as_posix())

        logger.info('Start fix address')
        for index, row in df.iterrows():
            try:
                if index % 100 == 0 and index > 0:
                    logger.info(f'Processed {index} rows')
                address_result = process_row(row)
                if address_result['error_status']:
                    append_row_to_csv(row.to_dict(), (output_dir / 'unprocessed_addresses.csv').as_posix())
                    continue
                df.loc[index, 'owner_google_county'] = address_result['county']
                df.loc[index, 'owner_google_country'] = address_result['country']
                df.loc[index, 'owner_google_city'] = address_result['city']
                df.loc[index, 'owner_google_state'] = address_result['state']
                df.loc[index, 'owner_google_zip'] = address_result['postal_code']
                df.loc[index, 'owner_google_zip_sufix'] = address_result['postal_code_sufix']
            except Exception as e:
                logger.info('Unexpected Error')
                logger.info(e)
        logger.info('End fix address')

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():

            logger.info("Creating table...")
            table_name = 'tmp_fix_address'
            df.to_sql(table_name, conn, "public", if_exists="replace")
            logger.info("Created temporary tmp_fix_address table")

        from manage import app
        with app.app_context():
            logger.info("Add columns")
            db.session.execute(
                f'''
                ALTER TABLE {table_name} ADD COLUMN subject_address_line_1 varchar;
                ALTER TABLE {table_name} ADD COLUMN subject_address_line_2 varchar;
                ALTER TABLE {table_name} ADD COLUMN subject_address_city varchar;
                ALTER TABLE {table_name} ADD COLUMN subject_address_state varchar;
                ALTER TABLE {table_name} ADD COLUMN subject_address_zip varchar;
                ALTER TABLE {table_name} ADD COLUMN property_id int;
                ALTER TABLE {table_name} ADD COLUMN tax_year int default 2020;
                ALTER TABLE {table_name} ADD COLUMN marketing_code_id int default 6;
                ALTER TABLE {table_name} ADD COLUMN subject_county varchar;
                ALTER TABLE {table_name} ADD COLUMN pin_code varchar;
                ALTER TABLE {table_name} ADD COLUMN application_type varchar default 'standard';
                '''
             )

            logger.info("Update subject address columns")
            db.session.execute(
                f'''
                update {table_name} as addr
                set
                    subject_address_line_1 = p.address_line_1,
                    subject_address_line_2 = p.address_line_2,
                    subject_address_city = p.city,
                    subject_address_state = p.state,
                    subject_address_zip = p.zip,
                    subject_county = p.county,
                    property_id = p.id
                from property p
                where p.apn = addr.legal_address;
                '''
            )
            db.session.commit()

        logger.info("Export result into file")
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():
            output_df = pd.read_sql(
                f"select * from {table_name};",
                conn
            )

        output_df['pin_code'] = output_df.apply(self.generate_pin_code, axis=1)
        self.mark_qr_code_columns(output_df)
        output_df.to_csv(output_dir / file_name)

    def generate_pin_code(self, row):
        try:
            property_id = int(row['property_id'])
            pin_code = PropertyService.generate_code(property_id)
            return pin_code
        except Exception as e:
            logger.error(e)
            return None

    def mark_qr_code_columns(self, df, sufix='(QR Code)'):
        df.rename(
            columns={
                'legal_address': 'legal_address' + sufix,
                'subject_county': 'subject_county' + sufix,
                'tax_year': 'tax_year' + sufix,
                'application_type': 'application_type' + sufix,
                'marketing_code_id': 'marketing_code_id' + sufix,
            },
            inplace=True
        )


def capitalize_address(address: str):
    def _capitalize(it):
        if it == '':
            return it
        if len(it) == 2:
            return it

        # 'FL33223' case
        elif len(it) == 7 and it[0:2].isalpha() and it[2:7].isnumeric():
            return it
        return it.capitalize()

    if not address:
        return address

    address = address.replace(',', '')
    splits = address.split(' ')
    items = []
    for i in range(len(splits) - 1):
        item = _capitalize(splits[i])
        items.append(item)

    if len(splits[-1]) == 2:
        last_item = splits[-1].capitalize()
    else:
        last_item = _capitalize(splits[-1])
    items.append(last_item)

    return ' '.join(items)


class CapitalizeAddress:

    def process_property_row(self, row):
        try:
            address = row['address'] if row['address'] else ''
            address_street = row['street'] if row['street'] else ''
            address_line_1 = row['address_line_1'] if row['address_line_1'] else ''
            address_line_2 = row['address_line_2'] if row['address_line_2'] else ''
            address_city = row['city'] if row['city'] else ''
            id = row['id']
            county = row['county']
            db.session.execute(
                f'''
                    update property as p
                    set
                        address = '{address}',
                        street = '{address_street}',
                        address_line_1 = '{address_line_1}',
                        address_line_2 = '{address_line_2}',
                        city = '{address_city}'
                    where p.id = {id}
                    and p.county = '{county}';
                '''
            )
            db.session.commit()
            logger.info(f'updated property address fields with id={id}')
        except Exception as e:
            logger.error(e.args)
        return row

    def process_owner_row(self, row):
        owner_address_1 = row['owner_address_1'] if row['owner_address_1'] else ''
        owner_address_2 = row['owner_address_2'] if row['owner_address_2'] else ''
        owner_address_3 = row['owner_address_3'] if row['owner_address_3'] else ''
        owner_city = row['owner_city'] if row['owner_city'] else ''
        id = row['id']

        db.session.execute(
            f'''
            update owner as o
            set
                owner_address_1 = '{owner_address_1}',
                owner_address_2 = '{owner_address_2}',
                owner_address_3 = '{owner_address_3}',
                owner_city = '{owner_city}'
            where o.id = {id};
            '''
        )
        db.session.commit()
        logger.info(f'updated owner address fields with id={id}')
        return row

    def capitalize_property_addresses(self, county, persist, csv, drop_table=True):
        logger.info(f'Process county: {county}')
        output_dir = DATA_IMPORT / 'output' / county
        output_dir.mkdir(parents=True, exist_ok=True)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():
            df = pd.read_sql(
                f"select id, address, street, address_line_1, address_line_2, city "
                f"from property "
                f"where county='{county}';",
                conn
            )
        df['address'] = df['address'].apply(capitalize_address)
        df['street'] = df['street'].apply(capitalize_address)
        df['address_line_1'] = df['address_line_1'].apply(capitalize_address)
        df['address_line_2'] = df['address_line_2'].apply(capitalize_address)
        df['city'] = df['city'].apply(capitalize_address)
        df['county'] = county

        if csv:
            df.to_csv(output_dir / f'{county}_property_addresses_capitalized.csv')

        if persist:
            engine = create_engine(SQLALCHEMY_DATABASE_URI)
            with engine.connect() as conn, conn.begin():

                logger.info("Creating table...")
                table_name = f'tmp_{county}_capitalize_address'
                df.to_sql(table_name, conn, "public", if_exists="replace")
                logger.info(f"Created temporary {table_name} table")

            from manage import app
            with app.app_context():

                logger.info("Update property address columns")
                db.session.execute(
                    f'''
                    update property as p
                    set
                        address = addr.address,
                        street = addr.street,
                        address_line_1 = addr.address_line_1,
                        address_line_2 = addr.address_line_2,
                        city = addr.city
                    from {table_name} addr
                    where p.id = addr.id
                    and p.county = '{county}';
                    '''
                )
                logger.info("Address fields updated")
                db.session.commit()

                if drop_table:
                    db.session.execute(f'''DROP TABLE {table_name};''')
                    logger.info(f"Delete temporary table {table_name}")
                    db.session.commit()

    def capitalize_owner_addresses(self, county, persist, csv, drop_table=True):
        logger.info(f'Process county: {county}')
        output_dir = DATA_IMPORT / 'output' / county
        output_dir.mkdir(parents=True, exist_ok=True)

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():
            df = pd.read_sql(
                f'''
                select owner.id, owner_address_1, owner_address_2, owner_address_3, owner_city from owner
                left join property p on owner.property_id = p.id
                where p.county='{county}';
                ''',
                conn
            )

        df['owner_address_1'] = df['owner_address_1'].apply(capitalize_address)
        df['owner_address_2'] = df['owner_address_2'].apply(capitalize_address)
        df['owner_address_3'] = df['owner_address_3'].apply(capitalize_address)
        df['owner_city'] = df['owner_city'].apply(capitalize_address)

        if csv:
            df.to_csv(output_dir / f'{county}_owner_addresses_capitalized.csv')

        if persist:
            engine = create_engine(SQLALCHEMY_DATABASE_URI)
            with engine.connect() as conn, conn.begin():

                logger.info("Creating table...")
                table_name = f'tmp_{county}_owner_capitalize_address'
                df.to_sql(table_name, conn, "public", if_exists="replace")
                logger.info(f"Created temporary {table_name} table")

            from manage import app
            with app.app_context():

                logger.info("Update owner address columns")
                db.session.execute(
                    f'''
                    update owner as o
                    set
                        owner_address_1 = addr.owner_address_1,
                        owner_address_2 = addr.owner_address_2,
                        owner_address_3 = addr.owner_address_3,
                        owner_city = addr.owner_city
                    from {table_name} addr
                    where o.id = addr.id;
                    '''
                )
                logger.info("Address fields updated")
                db.session.commit()

                if drop_table:
                    db.session.execute(f'''DROP TABLE {table_name};''')
                    logger.info(f"Delete temporary table {table_name}")
                    db.session.commit()


if __name__ == '__main__':
    # FixAddress().process_file(file_name='sample2_address_fix.csv')
    FixAddress().process_file(file_name='Miami and Broward 2nd Mailing List - 12k Prospects - 8.13.20.csv')
