from my_logger import logger
from app.data_import.florida import FileProcessor, execute_task, map_row, commit_sale
import pandas as pd
from app.data_import.nassau.sale import SaleProcessor
from app.database.models import Property
from app.database.models.sale import Sale, SaleValidation, BaseSaleSchema
from app.utils.constants import County


class SuffolkSaleProcessor(SaleProcessor):
    def __init__(self, county, file_name, schema, to_csv=False,
                 persist=False, owner=False):
        super().__init__(county, file_name, schema, to_csv=to_csv,
                         persist=persist, owner=owner)
        self.properties = Property.query.with_entities(
            Property.id,
            Property.print_key,
            Property.county,
            Property.undefined_field
        ) if self.persist else None

    def commit_sale(self, sale_map, errors):
        apn = sale_map.pop('apn')
        county = sale_map.pop('county')
        swis_code = sale_map.pop('swis_code')
        prop = self.properties.filter_by(print_key=apn,
                                         county=county,
                                         undefined_field=swis_code).first()
        if not prop:
            print(f'property with apn {apn} not in database')
        else:
            sale_map['property_id'] = prop.id
            Sale.insert(
                dict(property_id=sale_map['property_id'],
                     price=sale_map['price'],
                     date=sale_map['date'],
                     arms_length=sale_map['arms_length'],
                     seller_first_name=sale_map['seller_first_name'],
                     seller_last_name=sale_map['seller_last_name'],
                     buyer_first_name=sale_map['owner_first_name'],
                     buyer_last_name=sale_map['owner_last_name'])
            )
            if self.owner:
                SuffolkSaleProcessor.commit_owner(apn, county, prop.id, sale_map)
        if errors and sale_map:
            SaleValidation.insert(apn, county, errors)
        return None


class SuffolkSaleFileProcessor(FileProcessor):
    def __init__(self, file_name, persist, csv):
        super(SuffolkSaleFileProcessor, self).__init__(
            provider_name=County.SUFFOLK,
            table='sale',
            persist=persist,
            to_file=csv
        )
        self._file_name = file_name

    def prepare_data(self):
        input_path = self.input_dir() / self.file_name
        self.output_dir().mkdir(exist_ok=True, parents=True)

        df_original = pd.read_csv(input_path)
        df_original.to_csv(self.output_dir() / (self.file_name[:-4] + '_original.csv'))

        df = pd.read_csv(
            input_path,
            usecols=['APN', 'SELLER', 'BUYER', 'SALE_PRICE', 'SALE_DATE', 'ARMS_LENGT'],
            low_memory=False,
            dtype=str
        )
        df.rename(
            columns={
                'APN': "apn", "SELLER": "seller_first_name", "BUYER": "buyer_first_name", "SALE_PRICE": "price",
                "SALE_DATE": "date", "ARMS_LENGT": "arms_length",
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
        df.fillna('', inplace=True)
        df['arms_length'] = df['arms_length'].apply(lambda x: x.strip())
        df['arms_length'] = df['arms_length'].apply(lambda x: True if x == 'Y' else False)
        df['apn'] = df['apn'].apply(lambda x: x.strip())

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
    SuffolkSaleFileProcessor(
        file_name='dbo_Suffolk Sales VTable.txt',
        persist=False,
        csv=True
    ).process_file()
