import time

import pandas as pd
from sqlalchemy import create_engine

from app import db
from app.data_import.florida import FloridaAssessmentProcessor, FileProcessor
from app.data_import.miamidade.property import MiamidadePropertyProcessor
from app.data_import.processor import ProcessorOperation, PersistDataMixin
from app.utils.constants import County
from config import SQLALCHEMY_DATABASE_URI


class MiamidadeAssessmentProcessor(FloridaAssessmentProcessor):
    def __init__(self, nap_file_name: str, nal_file_name: str, persist: bool, to_file: bool):
        super(MiamidadeAssessmentProcessor, self).__init__(
            provider_name='miamidade',
            nap_file_name=nap_file_name,
            nal_file_name=nal_file_name,
            persist=persist,
            to_file=to_file
        )


class MiamidadeRollProcessor(FileProcessor, PersistDataMixin):
    """
    Read assessment information from inventory file, applied for the Tentative 2020
    """
    def __init__(self, persist, csv, file_name, assessment_type,
                 db_operation: ProcessorOperation = ProcessorOperation.INSERT, drop_imported: bool = True):
        super(MiamidadeRollProcessor, self).__init__(
            provider_name=County.MIAMIDADE,
            table='assessment',
            persist=persist,
            to_file=csv
        )
        self.drop_imported = drop_imported
        self._file_name = file_name
        self._assessment_type = assessment_type
        self.db_operation = db_operation

    def prepare_data(self):
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, skiprows=4, low_memory=False, names=MiamidadePropertyProcessor.col_names)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        print(f"Total data count: {len(df)}")

        return df

    def parse_data(self, df):
        df = df[df['year'] == 2020]
        df = df[['folio', 'year', 'assessed', 'sale_type_1', 'sale_qual_1', 'sale_date_1', 'sale_amt_1',
                 'sale_type_2', 'sale_qual_2', 'sale_date_2', 'sale_amt_2', 'sale_type_3', 'sale_qual_3',
                 'sale_date_3', 'sale_amt_3']]
        df.rename(columns={'folio': "apn"}, inplace=True)
        print(f"2020 data count: {len(df)}")

        # df.fillna('', inplace=True)

        df['assessment_type'] = self._assessment_type
        df['assessment_id'] = 10
        df['assessed'] = df['assessed'].astype(int)
        df["year"] = df['year'].astype(int)

        df['sale_date_1'] = pd.to_datetime(df['sale_date_1'])
        df['sale_date_2'] = pd.to_datetime(df['sale_date_2'])
        df['sale_date_3'] = pd.to_datetime(df['sale_date_3'])

        df['sale_amt_1'] = df['sale_amt_1'].astype(float)
        df['sale_amt_2'] = df['sale_amt_2'].astype(float)
        df['sale_amt_3'] = df['sale_amt_3'].astype(float)

        df['sale_type_1'] = df['sale_type_1'].astype(float)
        df['sale_type_2'] = df['sale_type_2'].astype(float)
        df['sale_type_3'] = df['sale_type_3'].astype(float)

        print(df.info())
        return df

    def update_assessments(self, assessment_date_id):
        """
        Update Miamidade assessments
        """
        file_path = self.input_dir() / self.file_name

        # import data csv file
        df = pd.read_csv(file_path, skiprows=4, low_memory=False, names=MiamidadePropertyProcessor.col_names)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df.rename(columns={'folio': "apn"}, inplace=True)
        df = df[['apn', 'total', 'assessed', 'year']]
        print(f"Total data count: {len(df)}")

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir() / f'{self.provider_name}_assessment_rolls.csv'
            df.to_csv(output_path)

        if self.persist:
            table_name = f'{self.provider_name}_assessment_rolls'
            schema = 'data_source'

            # create temporary table
            self.import_data(df, table_name, schema)
            self._create_property_id(table_name, schema)
            self._update_assessments(table_name, schema, assessment_date_id=assessment_date_id)

            if self.drop_imported:
                self.drop_data(table_name, schema)
            db.session.commit()

    def _update_assessments(self, table_name, schema, assessment_date_id):
        """
        Persist assessments changes to DB
        """
        sql = f'''
            update public.assessment a
            set (value, assessment_value) =
                (
                    rolls.total,
                    rolls.assessed
                )
            from {schema}.{table_name} rolls
            where rolls.property_id = a.property_id
            and a.assessment_id={assessment_date_id}
        '''
        db.session.execute(sql)
        print(f'updated {self.provider_name} assessments with assessment_id={assessment_date_id}')

    def process_file(self, **kwargs):
        df = self.prepare_data()
        df = self.parse_data(df)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / f'{self.provider_name}_assessments.csv', index=True, index_label='id')

        if self.persist:
            create_table = kwargs.get('create_table')
            update_table = kwargs.get('update_table')
            persist_assessments = kwargs.get('persist_assessments')
            persist_sales = kwargs.get('persist_sales')

            self.insert_assessments(df, create_table=create_table, update_table=update_table,
                                    persist_assessments=persist_assessments, persist_sales=persist_sales)

    def _create_table(self, df, table_name, schema='public'):
        start = time.time()
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():
            df.to_sql(table_name, conn, schema, method='multi', chunksize=10000, index=False, if_exists='replace')
            print(f"Created temporary '{table_name}' table in {time.time() - start} seconds")

    def _insert_assessments(self, table_name, schema):
        db.session.execute(
            f'''
        INSERT INTO public.assessment (value, assessment_type, property_id, assessment_id)
        SELECT assessed, assessment_type, property_id, assessment_id FROM {schema}.{table_name}
        where property_id is not null;
            '''
        )

    def _create_property_id(self, table_name, schema):
        db.session.execute(f'ALTER TABLE {table_name} ADD COLUMN property_id int;')
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

    def _insert_sales(self, table_name, schema):
        db.session.execute(
            f'''
            -- insert sale1 data into sale table
            INSERT INTO sale (property_id, price, date, arms_length)
            SELECT property_id, sale_amt_1, sale_date_1, arms_length1 FROM {schema}.{table_name}
            where property_id is not null
            and sale_amt_1 is not null;

            -- insert sale2 data into sale table
            INSERT INTO sale (property_id, price, date, arms_length)
            SELECT property_id, sale_amt_2, sale_date_2, arms_length2 FROM {schema}.{table_name}
            where property_id is not null
            and sale_amt_2 is not null;

            -- insert sale3 data into sale table
            INSERT INTO sale (property_id, price, date, arms_length)
            SELECT property_id, sale_amt_3, sale_date_3, arms_length3 FROM {schema}.{table_name}
            where property_id is not null
            and sale_amt_3 is not null;

            '''
        )
        print('sales inserted')

    def _create_arms_length(self, table_name, schema):
        db.session.execute(
            f'''
            ALTER TABLE {schema}.{table_name} ADD COLUMN arms_length1 bool default false;
            ALTER TABLE {schema}.{table_name} ADD COLUMN arms_length2 bool default false;
            ALTER TABLE {schema}.{table_name} ADD COLUMN arms_length3 bool default false;

            -- update arms_length1
            update {schema}.{table_name}
            set arms_length1=true
            where sale_qual_1='Q';

            -- update arms_length2
            update {schema}.{table_name}
            set arms_length2=true
            where sale_qual_2='Q';

            -- update arms_length3
            update {schema}.{table_name}
            set arms_length3=true
            where sale_qual_3='Q';
            '''
        )
        print('arms_length created and updated')

    def insert_assessments(self, df, create_table: bool = True, update_table: bool = True,
                           persist_assessments: bool = True, persist_sales: bool = True):
        """
        Persist prepared data rolls using RAW SQL which is much faster than row by row
        """
        try:
            table_name = f'{self.provider_name}_assessments'
            schema = 'data_source'

            if create_table:
                # create temporary table
                self.import_data(df, table_name, schema)
            if update_table:
                # add property_id and link with property table to be sure we process only
                # data for the properties we have in database
                self._create_property_id(table_name, schema)

                if persist_assessments:
                    # ensure! that previously created required assessment_date record in database
                    # also is required to create assessment file in assessment_files table
                    # insert only records for existed properties in a system
                    self._insert_assessments(table_name, schema)

                if persist_sales:
                    self._create_arms_length(table_name, schema)
                    self._insert_sales(table_name, schema)

            if self.drop_imported:
                self.drop_data(table_name, schema)

            db.session.commit()

        except Exception as e:
            print(e.args)


class MiamidadeCompareAssessments(FileProcessor, PersistDataMixin):
    def __init__(self, old_file_name, new_file_name, persist, csv, drop_imported):
        super(MiamidadeCompareAssessments, self).__init__(
            provider_name=County.MIAMIDADE,
            table='assessment',
            persist=persist,
            to_file=csv
        )
        self.drop_imported = drop_imported
        self.old_file_name = old_file_name
        self.new_file_name = new_file_name

    @staticmethod
    def prepare_data(file_path):
        # import data csv file
        df = pd.read_csv(file_path, skiprows=4, low_memory=False, names=MiamidadePropertyProcessor.col_names)

        # delete last row
        df.drop(df.tail(1).index, inplace=True)
        df = df[['folio', 'total', 'assessed']]
        print(f"Total data count: {len(df)}")

        return df

    def compare(self):
        old_file_path = self.input_dir() / self.old_file_name
        new_file_path = self.input_dir() / self.new_file_name

        df_old = self.prepare_data(file_path=old_file_path)
        df_old.rename(columns={'total': "total_old", "assessed": "assessed_old"}, inplace=True)

        df_new = self.prepare_data(file_path=new_file_path)
        df_new.rename(columns={'total': "total_new", "assessed": "assessed_new"}, inplace=True)

        # inner join of two dataframes by apn
        df = pd.merge(df_old, df_new, how='inner', on=['folio'])
        print(f'Joined count: {len(df)}')

        import numpy as np
        df['compare_total'] = np.where((df['total_old'] != df['total_new']), True, False)
        df['compare_assessed'] = np.where((df['assessed_old'] != df['assessed_new']), True, False)

        if self.to_file:
            self.output_dir().mkdir(parents=True, exist_ok=True)
            df.to_csv(self.output_dir() / f'{self.provider_name}_assessments_compared.csv', index=False)

        if self.persist:
            table_name = f'{self.provider_name}_assessments_compared'
            schema = 'data_source'
            self.import_data(df, table_name, schema=schema)

            df = self.get_all_assessment_changes()
            print(f'Total assessments changes count: {len(df)}')
            df.to_csv(self.output_dir() / 'assessments_changes.csv', index=False)

            df = self.get_case_changes()
            print(f'Total cases assessments changes count: {len(df)}')
            df.to_csv(self.output_dir() / 'cases_assessments_changes.csv', index=False)

            if self.drop_imported:
                self.drop_data(table_name, schema)

            db.session.commit()

    @staticmethod
    def get_all_assessment_changes():
        """
        Select properties where assessment values were changed
        """
        sql = '''
            select p.id as property_id, p.apn, m.total_old, m.total_new, m.assessed_old, m.assessed_new
            from data_source.miamidade_assessments_compared1 m
            join property p on p.apn = m.folio
            where assessed_new != assessed_old
            or total_new != total_old;
        '''
        changed_rows = db.session.execute(sql)

        df = pd.DataFrame(changed_rows.fetchall())
        df.columns = changed_rows.keys()

        return df

    @staticmethod
    def get_case_changes():
        """
        Select cases information where assessment values were changed
        """
        sql = '''
            select cp.property_id, cp.apn, m.total_old, m.total_new, m.assessed_old, m.assessed_new
            from case_property cp
            join property p on cp.property_id = p.id
            join data_source.miamidade_assessments_compared1 m on m.folio = p.apn
            where m.assessed_new != m.assessed_old
            or m.total_new != m.total_old;
        '''

        changed_rows = db.session.execute(sql)

        df = pd.DataFrame(changed_rows.fetchall())
        df.columns = changed_rows.keys()

        return df
