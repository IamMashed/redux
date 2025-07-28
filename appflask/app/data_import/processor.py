from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from app import db
from config import SQLALCHEMY_DATABASE_URI


class ProcessorOperation:
    """
    Define database processor operations
    """
    INSERT = 'insert'
    UPDATE = 'update'
    UPDATE_IF_EXISTS = 'update_if_exists'
    UPSERT = 'insert_new_or_update_if_exists'


class ProcessorSettings:
    """
    Processor settings class
    """
    def __init__(self, persist=False, to_file=True, operation=ProcessorOperation.INSERT, use_cols=None,
                 persist_validation_errors=False, drop_imported: bool = False):
        self.operation = operation
        self.persist = persist
        self.to_file = to_file
        self.use_cols = use_cols
        self.persist_validation_errors = persist_validation_errors
        self.drop_imported = drop_imported


class PersistDataMixin:
    def import_data(self, df, table_name, schema, chunksize=50000, progress_bar=True):
        """
        Import dataframe to Database
        """
        import time
        start = time.time()
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():

            if progress_bar:
                # chunksize = int(len(df) / 10)  # 10%
                with tqdm(total=len(df)) as pbar:
                    for i, chunk in enumerate(self.make_chunks(df, chunksize)):
                        replace = "replace" if i == 0 else "append"
                        chunk.to_sql(table_name, conn, schema, method='multi', if_exists=replace, index=False,
                                     chunksize=len(chunk))
                        pbar.update(len(chunk))
            else:
                df.to_sql(table_name, conn, schema, method='multi', chunksize=chunksize, index=False,
                          if_exists='replace')
            print(f"Data imported to '{table_name}' table")
            print(f'Import time: {time.time() - start} seconds')

    def drop_data(self, table_name, schema):
        """
        Delete table from DB
        Option:
            - prevented deleting from 'public' schema
        """
        if schema == 'public':
            raise IntegrityError("Prevented to delete from 'public' schema for security reason")
        else:
            db.session.execute(f'''DROP TABLE IF EXISTS {schema}.{table_name};''')
            print(f"Deleted imported table '{table_name}' from {schema} schema")

    def insert_data(self, *args, **kwargs):
        pass

    def update_data(self, *args, **kwargs):
        pass

    def make_chunks(self, seq, size):
        # from http://stackoverflow.com/a/434328
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))
