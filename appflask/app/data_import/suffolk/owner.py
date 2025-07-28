from app.data_import.suffolk.assessment import Processor
import pandas as pd

from app.database.models import Property, Owner
from app.database.models.owner import OwnerValidation
from config import DATA_IMPORT

pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.width = None


class OwnerProcessor(Processor):
    # assessment owner processor

    def commit_row(self, row):
        with self.app.app_context():
            errors = dict()
            prop = Property.query.filter_by(apn=row.par_id).first()
            if not prop:
                errors['property'] = f'property with apn {row.par_id} not in database'
            else:
                error_at_db = Owner.insert(
                    dict(data_source='assessment',
                         property_id=prop.id,
                         created_on=row.sale_date,
                         first_name=row.owner_first_name,
                         last_name=row.owner_last_name,
                         owner_address_1=row.address,
                         owner_city=row.mail_city,
                         owner_zip=row.mail_zip
                         )
                )
                if error_at_db:
                    errors['database_operation'] = error_at_db

            if errors:
                OwnerValidation.insert(
                    row.par_id, 'suffolk', errors)

    def join_dataframes(self):
        source_folder = DATA_IMPORT / 'src' / self.folder_name / 'property'
        first = source_folder / 'owner.txt'
        first_df = pd.read_csv(first,
                               usecols=['muni_code',
                                        'parcel_id',
                                        'owner_id',
                                        'owner_first_name',
                                        'owner_last_name',
                                        'mail_st_rte',
                                        'mail_st_nbr',
                                        'owner_mail_st_stuff',
                                        'post_dir',
                                        'mail_city',
                                        'owner_mail_state',
                                        'mail_zip'],
                               low_memory=False,
                               dtype={'mail_zip': str})
        first_df.fillna('', inplace=True)

        second = source_folder / 'parcel_to_owner.txt'
        second_df = pd.read_csv(second,
                                usecols=["muni_code",
                                         "parcel_id",
                                         "owner_id",
                                         "sale_date"])
        df = pd.merge(first_df, second_df, how='left',
                      on=['owner_id', 'muni_code', 'parcel_id'])

        third = source_folder / 'parcel_parid.txt'
        third_df = pd.read_csv(third,
                               usecols=['muni_code',
                                        'parcel_id',
                                        'par_id'],
                               dtype={'par_id': str})
        df = pd.merge(df, third_df, how='left',
                      on=['parcel_id', 'muni_code'])

        df['address'] = df['mail_st_rte'] + ' ' + df['mail_st_nbr'] + ' ' + df['owner_mail_st_stuff'] + ' ' + df[
            'post_dir'] + ' ' + df['mail_city'] + ' ' + df['owner_mail_state'] + ' ' + df['mail_zip']
        df['address'] = df['address'].apply(str.strip)
        del df['mail_st_rte']
        del df['mail_st_nbr']
        del df['owner_mail_st_stuff']
        del df['post_dir']
        # del df['mail_city']
        del df['owner_mail_state']
        # del df['mail_zip']

        if self.csv_output:
            self.store_as_csv(df)

        return df
