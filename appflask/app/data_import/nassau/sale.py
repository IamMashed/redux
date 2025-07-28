from my_logger import logger
from sqlalchemy.exc import IntegrityError

from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from csv import reader, writer

import click
import pandas as pd
from marshmallow import EXCLUDE, ValidationError

from app import db
from app.data_import.florida import FileProcessor, map_row, execute_task, commit_sale, commit_owner
from app.data_import.palmbeach.data_loading import append_row_to_csv
from app.database.models import Property, Owner, OwnerValidation
from app.database.models.owner import OwnerSchema
from app.database.models.sale import Sale, SaleValidation, BaseSaleSchema
from app.utils.constants import County
from config import DATA_IMPORT, MAX_WORKER_COUNT


class NassauCUWSaleProcessor(FileProcessor):
    def __init__(self, file_name, persist, to_file, owner):
        super().__init__(
            provider_name='nassau',
            table='sale',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name
        self.owner = owner

    def process_input_file(self):
        file_path = self.input_dir() / self.file_name
        df = pd.read_csv(file_path, encoding="ISO-8859-1", header=0, low_memory=False)
        df.fillna('', inplace=True)

        # export input file to outputs as .csv format
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / (self.file_name[:-4] + '.csv'), index=False)

        execute_task(self.process_row, df.iterrows(), total=len(df.index), desc=f"process {self.file_name}")

    def process_row(self, row):

        # parse gis row
        parsed_row = self.parse_row(row)

        # map Sale data with marshmallow schema
        sale_map, sale_errors = map_row(parsed_row, BaseSaleSchema)
        owner_map, owner_errors = map_row(parsed_row, OwnerSchema)

        # export to db
        if self.persist:
            # update sale price if exist or insert new
            self.upsert_sale(sale_map, sale_errors)

            # update or insert owner
            if self.owner:
                self.upsert_owner(owner_map, owner_errors)

        # export to csv
        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / (self.file_name[:-4] + '_parsed.csv')
            append_row_to_csv(parsed_row, output_path.as_posix())

    def parse_row(self, row) -> dict:
        row_data = dict()
        row_data['apn'] = row.PARID.strip()
        row_data['county'] = self.provider_name

        row_data.update(self._parse_sale_fields(row))
        row_data.update(self._parse_owner_fields(row))

        return row_data

    def upsert_sale(self, fields_map, errors):
        """
        Insert new sale object to database or update only sale price if exists.
        :param fields_map: The sale object fields map
        :param errors: The validation errors if any
        """

        if errors is None:
            errors = dict()

        apn = fields_map.get('apn')
        county = fields_map.get('county')

        from manage import app
        with app.app_context():
            prop_obj = Property.query.filter_by(apn=apn, county=county).first()

            if not prop_obj:
                errors['property'] = f'property with apn {apn} not in database'
            else:
                sale_obj = Sale.query.filter_by(property_id=prop_obj.id, date=fields_map['date']).first()
                if not sale_obj:
                    # no sale found for the property, insert new
                    fields_map['property_id'] = prop_obj.id

                    if self.to_file:
                        self.output_dir().mkdir(exist_ok=True, parents=True)
                        append_row_to_csv(fields_map, (self.output_dir() / 'new_sales.csv').as_posix())
                    # persist new sale
                    commit_sale(fields_map, errors)
                else:
                    # sale conflict found for the property, update sale price only
                    fields_to_update = dict(
                        apn=apn,
                        county=county,
                        property_id=prop_obj.id,
                        price=fields_map['price'],
                        buyer_first_name=fields_map['buyer_first_name'],
                        buyer_last_name=fields_map['buyer_last_name'],
                        seller_first_name=fields_map['seller_first_name'],
                        seller_last_name=fields_map['seller_last_name']
                    )
                    commit_sale(fields_to_update, errors, upsert=True)

            # if errors and fields_map:
            #     SaleValidation.insert(apn, county, errors)

        return None

    def upsert_owner(self, fields_map, errors):
        """
        Update owner if exist or insert new
        :param fields_map:
        :param errors:
        :return:
        """
        if errors is None:
            errors = dict()

        apn = fields_map.get('apn')
        county = fields_map.get('county')

        from manage import app
        with app.app_context():
            prop_obj = Property.query.filter_by(apn=apn, county=county).first()

            if not prop_obj:
                errors['property'] = f'property with apn {apn} not in database'
            else:
                owner_obj = Owner.query.filter_by(property_id=prop_obj.id, data_source='sale').first()
                if not owner_obj:
                    # no owner found, insert new
                    fields_map['property_id'] = prop_obj.id
                    commit_owner(fields_map, errors)

                    if self.to_file:
                        self.output_dir().mkdir(parents=True, exist_ok=True)
                        append_row_to_csv(fields_map, (self.output_dir() / 'new_owners.csv').as_posix())
                else:
                    # owner found for the sale, update owner
                    fields_map['property_id'] = prop_obj.id
                    fields_map.pop('apn')
                    fields_map.pop('county')

                    # exclude None values
                    to_update = {k: v for k, v in fields_map.items() if v is not None}
                    update_error = self.update_owner(to_update)

                    if update_error:
                        errors['database_operation'] = update_error

            if errors and fields_map:
                OwnerValidation.insert(apn, county, errors)

        return None

    def update_owner(self, object_map):
        """
        Update owner if exist.
        """
        obj = Owner.query.filter_by(property_id=object_map['property_id'], data_source='sale')
        try:
            if obj.first():  # update if exists
                obj.update({**object_map})
                # print(f'owner updated record with property_id {object_map["property_id"]}')
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f'failed to upsert due to {e.orig.args}')
            return e.orig.args
        return None

    def _parse_sale_fields(self, row) -> dict:
        row_data = dict()
        row_data['price'] = self._parse_sale_price(row.SALESPRIC)
        row_data['date'] = self._parse_sale_date(row.SALESDATE)
        row_data['arms_length'] = True if row.ARMS == 'Y' else False
        row_data['buyer_first_name'] = row.BUY_FNAME
        row_data['buyer_last_name'] = row.BUY_LNAME
        row_data['seller_first_name'] = row.SELL_FNAME
        row_data['seller_last_name'] = row.SELL_LNAME
        return row_data

    def _parse_owner_fields(self, row) -> dict:
        row_data = dict()
        row_data['data_source'] = self.table
        row_data['created_on'] = self._parse_sale_date(row.SALESDATE)
        row_data['own_first_name'] = row.BUY_FNAME
        row_data['own_last_name'] = row.BUY_LNAME

        return row_data

    def _parse_sale_price(self, value) -> float:
        if value is None or value == '':
            return 0.0
        return float(value)

    def _parse_sale_date(self, value):
        dt = pd.to_datetime(value, format='%m/%d/%Y %H:%M:%S')
        return str(dt.date())


class SaleProcessor:

    def __init__(self, county, file_name, schema, owner=False,
                 to_csv=False, persist=False):
        self.county = county
        self.file_name = file_name
        self.to_csv = to_csv
        self.persist = persist
        self.owner = owner
        self.schema = schema(unknown=EXCLUDE)
        self.properties = Property.query.with_entities(
            Property.id, Property.apn, Property.county
        ) if self.persist else None

    @staticmethod
    def commit_owner(apn, county, property_id, sale_map):
        # insert Owner
        owner_error_at_insert = Owner.insert(
            dict(data_source='sale',
                 property_id=property_id,
                 created_on=sale_map['date'],
                 first_name=sale_map['owner_first_name'],
                 last_name=sale_map['owner_last_name'],
                 street_address=sale_map['owner_address'],
                 second_owner_last_name=sale_map['second_owner_last_name']
                 )
        )
        if owner_error_at_insert:
            owner_errors = dict()
            owner_errors['owner_database_operation'] = owner_error_at_insert
            OwnerValidation.insert(apn, county, owner_errors)
        return None

    def commit_sale(self, sale_map, errors):
        apn = sale_map.pop('apn')
        county = sale_map.pop('county')
        sale_map.pop('swis_code')
        prop = self.properties.filter_by(apn=apn,
                                         county=county).first()
        if not prop:
            errors['property'] = f'property with apn {apn} not in database'
        else:
            sale_map['property_id'] = prop.id
            error_at_update = Sale.insert(
                dict(property_id=sale_map['property_id'],
                     price=sale_map['price'],
                     date=sale_map['date'],
                     arms_length=sale_map['arms_length'],
                     seller_first_name=sale_map['seller_first_name'],
                     seller_last_name=sale_map['seller_last_name'],
                     buyer_first_name=sale_map['owner_first_name'],
                     buyer_last_name=sale_map['owner_last_name'])
            )
            if error_at_update:
                errors['database_operation'] = error_at_update

            # insert Owner
            if self.owner:
                SaleProcessor.commit_owner(apn, county, prop.id, sale_map)

        if errors and sale_map:
            SaleValidation.insert(apn, county, errors)

        return None

    def map_row(self, columns, row):
        raw_data = dict(zip(columns, row))

        error_messages = dict()
        try:
            sales_map = self.schema.load(raw_data)
        except ValidationError as e:
            error_messages = e.messages
            sales_map = e.valid_data

        if self.persist:
            from manage import app
            with app.app_context():
                self.commit_sale(sales_map, error_messages)
        return sales_map

    def combine_to_csv_sample(self, columns, csv_reader):
        """
        Write first ten lines to a csv file for
        presentation of proper mapping
        :param columns: header of csv
        :param csv_reader: csv reader
        :return: None
        """
        output_folder = DATA_IMPORT / 'output' / self.county / 'sale'
        output_folder.mkdir(parents=True, exist_ok=True)
        path = output_folder / self.file_name
        count = 0
        with open(path, 'w+') as f:
            w = writer(f)
            next_row = self.map_row(columns, next(csv_reader))
            w.writerow(next_row.keys())
            while True:
                count += 1
                if count == 100:
                    break
                try:
                    next_row = self.map_row(
                        columns, next(csv_reader))
                    w.writerow(next_row.values())
                except StopIteration:
                    break
        return None

    def async_store_to_database(self, columns, csv_reader):
        with ThreadPoolExecutor(MAX_WORKER_COUNT) as executor:
            futures = [
                executor.submit(self.map_row, columns, row)
                for row in csv_reader
            ]
            print('sales futures submitted')

            with click.progressbar(
                    length=csv_reader.line_num,
                    label='processing sales') as bar:
                for _ in as_completed(futures):
                    bar.update(1)
        return None

    def process_input_file(self):
        input_path = DATA_IMPORT / 'src' / self.county / 'sale' / self.file_name
        with open(input_path) as f:
            csv_reader = reader(f)
            columns = next(csv_reader)
            if self.to_csv:
                self.combine_to_csv_sample(columns, csv_reader)
            if self.persist:
                self.async_store_to_database(columns, csv_reader)
        return None


class NassauSaleFileProcessor(FileProcessor):
    def __init__(self, file_name, persist, csv):
        super(NassauSaleFileProcessor, self).__init__(
            provider_name=County.NASSAU,
            table='sale',
            persist=persist,
            to_file=csv
        )
        self._file_name = file_name

    def prepare_data(self):
        input_path = self.input_dir() / self.file_name
        df_original = pd.read_csv(input_path)

        self.output_dir().mkdir(exist_ok=True, parents=True)
        df_original.to_csv(self.output_dir() / (self.file_name[:-4] + '_original.csv'))

        df = pd.read_csv(
            input_path,
            usecols=['SALESPRIC', 'SALESDATE', 'BUY_LNAME', 'BUY_FNAME', 'SELL_LNAME', 'SELL_FNAME', 'ARMS', 'PARID'],
            low_memory=False,
        )
        df.rename(
            columns={
                'PARID': "apn", "SALESPRIC": "price", "SALESDATE": "date", "ARMS": "arms_length",
                "BUY_LNAME": "buyer_last_name", "BUY_FNAME": "buyer_first_name",
                "SELL_LNAME": "seller_first_name", "SELL_FNAME": "seller_first_name",
            },
            inplace=True
        )
        df['county'] = self.provider_name

        logger.info(f"Columns: {df.columns}")
        logger.info(df.info())

        # prepare sale date data
        df['date'] = df['date'].astype('datetime64')
        df['date'] = df['date'].apply(lambda x: str(x.date()))

        # prepare arms_length data
        df['apn'] = df['apn'].apply(lambda x: x.strip())
        df.fillna('', inplace=True)
        df['arms_length'] = df['arms_length'].apply(lambda x: x.strip())
        df['arms_length'] = df['arms_length'].apply(lambda x: True if x == 'Y' else False)

        return df

    def process_file(self):
        self.output_dir().mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir() / (self.file_name[:-4] + ".csv")

        df = self.prepare_data()
        if self.to_file:
            df.to_csv(output_path)

        if self.persist:
            execute_task(self.process_row, iterator=df.iterrows(), total=len(df.index),
                         desc=f"Process {self.file_name}")

    def process_row(self, row):
        # map Sale data with marshmallow schema
        sale_map, sale_errors = map_row(row.to_dict(), BaseSaleSchema)
        # insert sales
        commit_sale(sale_map, sale_errors, upsert=False)
        return sale_map


if __name__ == '__main__':
    NassauSaleFileProcessor(
        file_name='NASS_sale.txt',
        persist=False,
        csv=True
    ).process_file()
