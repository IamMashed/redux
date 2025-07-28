import csv
import pandas as pd
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

import click

from app import db
from app.data_import.florida import map_row
from app.data_import.processor import PersistDataMixin, ProcessorOperation
from app.database.models import Property, Owner, OwnerValidation
from app.database.models.owner import OwnerSchema
from app.database.models.property import PropertyValidation
from config import DATA_IMPORT, MAX_WORKER_COUNT

from marshmallow import EXCLUDE, ValidationError

from app.database.models.assessment import (
    BaseRecord400Schema,
    TotalTaxRecord405Schema,
    Exemptions410Schema,
    TaxAuthority420Schema,
    DirectAssessment430Schema,
    RestoredTaxes440Schema,
    DisputedFund450Schema,
    DisputedFundSchema460Schema,
    Assessment,
    AssessmentValidation)


class NassauAssessmentProcessor(PersistDataMixin):

    def __init__(self, folder_name, assessment_type_id, assessment_date_id, to_file=True, persist=False,
                 drop_imported=True):
        """
        There will be three folder names to process
        Final, Tent and School
        :param folder_name:
        """
        assert folder_name in ['final', 'school', 'tent', 'tent_2019', 'tent_2020', 'tent_2021', 'school_2020',
                               'final_2020']
        self.folder_name = folder_name
        self.properties = Property.query.with_entities(
            Property.id, Property.apn, Property.county
        )
        self.assessment_type_id = assessment_type_id
        self.assessment_date_id = assessment_date_id
        self.to_file = to_file
        self.persist = persist
        self.drop_imported = drop_imported

    @staticmethod
    def process_type_400(row):
        """Base record or General Data"""
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            crc1=row[37:42].strip(),
            crc1_pct=row[42:52].strip(),
            crc2=row[52:57].strip(),
            crc2_pct=row[57:67].strip(),
            crc3=row[67:72].strip(),
            crc3_pct=row[72:82].strip(),
            crc4=row[82:87].strip(),
            crc4_pct=row[87:97].strip(),
            crc5=row[97:102].strip(),
            crc5_pct=row[102:112].strip(),
            crc6=row[112:117].strip(),
            crc6_pct=row[117:127].strip(),
            village_1=row[127:130].strip(),
            village_1_pct=row[130:140].strip(),
            village_2=row[140:143].strip(),
            village_2_pct=row[143:153].strip(),
            village_3=row[153:156].strip(),
            village_3_pct=row[156:166].strip(),
            owner_1=row[166:206].strip(),
            owner_2=row[206:246].strip(),
            care_of=row[246:306].strip(),
            owner_address_1=row[306:406].strip(),
            owner_address_2=row[406:506].strip(),
            owner_address_3=row[506:606].strip(),
            property_address=row[606:706].strip(),
            property_address_2=row[706:806].strip(),
            lot=row[806:836].strip(),
            property_desc=row[836:840].strip(),
            property_class=row[840:841].strip(),
            property_desc_2=row[841:881].strip(),
            book=row[881:889].strip(),
            page=row[889:897].strip(),
            swiss_code=row[897:905].strip(),
            state_school_district=row[905:913].strip(),
            roll_section=row[913:915].strip(),
            excluded=row[915:916].strip(),
            prior_year_land_total=row[916:928].strip(),
            prior_year_total_assessment=row[928:940].strip(),
            total_land_assessment=row[940:952].strip(),
            total_assessment=row[952:964].strip(),
            total_market_value=row[964:976].strip(),
            equalization_ratio=row[977:984].strip(),
            t_code_amount=row[984:996].strip(),
            acres=row[996:1009].strip(),
            square_foot=row[1009:1019].strip()
        )

    @staticmethod
    def process_type_405(row):
        """Total Tax Record or Tax File Header"""
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            tax_before_abatement_or_star=row[37:50].strip(),
            abatement_or_star=row[50:63].strip(),
            first_half_tax=row[63:76].strip(),
            second_half_tax=row[76:89].strip(),
            total_tax=row[89:102].strip(),
            exemption_count=row[102:104].strip(),
            tax_or_authority_count=row[104:106].strip(),
            direct_assessment_count=row[106:108].strip(),
            restored_tax_count=row[108:110].strip()
        )

    @staticmethod
    def process_type_410(row):
        """Exemption Data"""
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            code=row[37:42].strip(),
            description=row[42:72].strip(),
            amount=row[72:82].strip(),
            computed_star=row[82:92].strip(),
            capped_star=row[92:102].strip(),
            actual_star=row[102:112].strip(),
            star_difference=row[112:122].strip()
        )

    @staticmethod
    def process_type_420(row):
        """Tax or authority data"""
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            authority_code=row[37:43].strip(),
            authority_description=row[43:83].strip(),
            total_assessment=row[83:93].strip(),
            exempt_assessment=row[93:103].strip(),
            taxable_assessment=row[103:113].strip(),
            tax_rate=row[113:124].strip(),
            tax_amount=row[124:137].strip(),
            tax_district=row[137:142].strip()
        )

    @staticmethod
    def process_type_430(row):
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            project_number=row[38:42].strip(),
            project_description=row[43:73].strip(),
            tax_amount=row[73:86].strip()
        )

    @staticmethod
    def process_type_440(row):
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            exemption_code=row[37:42].strip(),
            description=row[42:72].strip(),
            tax_year=row[72:76].strip(),
            tax_amount=row[76:89].strip()
        )

    @staticmethod
    def process_type_450(row):
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            tax_year=row[37:41].strip(),
            daf_percentage=row[41:46].strip(),
            daf_school_taxable=row[46:56].strip(),
            daf_town_taxable=row[56:66].strip(),
            daf_county_taxable=row[66:76].strip(),
            daf_school_deduction=row[76:89].strip(),
            daf_general_deduction=row[89:102].strip(),
            daf_school_fund=row[102:115].strip(),
            daf_general_fund=row[115:128].strip()
        )

    @staticmethod
    def process_type_460(row):
        return dict(
            record_type=row[0:3].strip(),
            town_code=row[3:4].strip(),
            school_district=row[4:7].strip(),
            parid=row[7:37].strip(),
            tax_year=row[37:41].strip(),
            star_amount=row[41:54].strip()
        )

    process_functions = {
        400: process_type_400.__func__,
        405: process_type_405.__func__,
        410: process_type_410.__func__,
        420: process_type_420.__func__,
        430: process_type_430.__func__,
        440: process_type_440.__func__,
        450: process_type_450.__func__,
        460: process_type_460.__func__,
    }

    mapping_schemas = {
        400: BaseRecord400Schema,
        405: TotalTaxRecord405Schema,
        410: Exemptions410Schema,
        420: TaxAuthority420Schema,
        430: DirectAssessment430Schema,
        440: RestoredTaxes440Schema,
        450: DisputedFund450Schema,
        460: DisputedFundSchema460Schema,
    }

    def _pop_village_fields(self, assessment_map):
        fields = dict()

        fields['apn'] = assessment_map.get('apn')
        fields['county'] = assessment_map.get('county')

        fields['village'] = assessment_map.pop('village_1')
        assessment_map.pop('village_1_pct')
        assessment_map.pop('village_2')
        assessment_map.pop('village_2_pct')
        assessment_map.pop('village_3')
        assessment_map.pop('village_3_pct')

        return fields

    def _pop_owner_fields(self, assessment_map):
        fields = dict()

        fields['apn'] = assessment_map.get('apn')
        fields['county'] = assessment_map.get('county')

        fields['data_source'] = 'assessment'
        # TODO: what date owner was created? Same as assessment?
        fields['created_on'] = '2019-09-01'
        fields['own_first_name'] = assessment_map.pop('owner_1')
        fields['own_second_owner_first_name'] = assessment_map.pop('owner_2')
        fields['own_address_1'] = assessment_map.pop('owner_address_1')
        fields['own_address_2'] = assessment_map.pop('owner_address_2')
        fields['own_address_3'] = assessment_map.pop('owner_address_3')

        # parse owner city, zip from 'owner_address_3'
        fields['own_zip'] = self._parse_owner_zip(fields['own_address_3'])
        fields['own_city'] = self._parse_owner_city(fields['own_address_3'])

        return fields

    def _parse_owner_city(self, address):
        if not self._valid_address(address):
            return None

        splits = address.split()
        city = ''
        for i in range(len(splits) - 2):
            city += ' ' + splits[i]

        return city.strip()

    def _parse_owner_zip(self, address: str):
        if not self._valid_address(address):
            return None

        return address.split()[-1][0:5]

    def _valid_address(self, address) -> bool:
        if address is None or address == "":
            return False

        # address should be in format: "<city> <state> <zip>"
        if len(address.split()) < 3:
            return False

        return True

    def commit_assessment(self, assessment_map, errors):
        apn = assessment_map.pop('apn')
        county = assessment_map.pop('county')
        prop = self.properties.filter_by(apn=apn,
                                         county=county).first()

        if not prop:
            errors['property'] = f'property with {apn} not in database'
            print(f'attempt to commit assessment but property with apn {apn} not in database')
        else:
            # store the assessment
            assessment_map['property_id'] = prop.id
            assessment_map['assessment_id'] = 7
            error_at_update = Assessment.insert(
                assessment_map)

            if error_at_update:
                errors['database_operation'] = error_at_update

        if errors and assessment_map:
            AssessmentValidation.insert(apn, county, errors)

        return None

    def map_using_schema(self, line, raw_data, schema, persist=False):
        """
        Map and optionally commit each row to the database
        :param line: string representation of data. used for click progress bar
        :param raw_data: sliced data as dict
        :param schema: schema instance for mapping
        :param persist: whether you need to persist in database or not
        :return: tuple of raw line as string and mapped data
        """
        # convert all empty string values to None
        raw_data = {k: None if not v else v for
                    k, v in raw_data.items()}
        raw_data['assessment_type'] = 'tent'
        error_messages = dict()
        try:
            mapped_data = schema.load(raw_data)
        except ValidationError as e:
            error_messages = e.messages
            mapped_data = e.valid_data

        # pop village fields
        village_fields = self._pop_village_fields(mapped_data)

        # pop owner fields
        owner_data = self._pop_owner_fields(mapped_data)
        owner_map, owner_errors = map_row(owner_data, OwnerSchema)

        if persist:
            from manage import app
            with app.app_context():

                # commit assessment
                self.commit_assessment(mapped_data, error_messages)

                # commit villages to 'property' table
                self.commit_villages(village_fields, error_messages)

                # commit owner data to 'owner' table
                self.commit_owner(owner_map, owner_errors)

        return mapped_data, line

    def commit_villages(self, fields, errors):
        apn = fields['apn']
        county = fields['county']

        prop = self.properties.filter_by(apn=apn, county=county).first()

        if not prop:
            errors['property'] = f'property with {apn} not in database'
        else:
            update_error = Property.update_if_exists(fields)

            if update_error:
                property_error = dict()
                property_error['database_operation'] = update_error
                PropertyValidation.insert(apn, county, property_error)

        if errors and fields:
            PropertyValidation.insert(apn, county, errors)

        return None

    def commit_owner(self, fields, errors):
        if errors is None:
            errors = dict()

        apn = fields.pop('apn')
        county = fields.pop('county')

        prop = self.properties.filter_by(apn=apn, county=county).first()

        if not prop:
            errors['property'] = f'property with {apn} not in database'
        else:
            # store the assessment owner
            fields['property_id'] = prop.id
            owner_persist_error = Owner.update_if_exists(fields)

            if owner_persist_error:
                owner_error = dict()
                owner_error['database_operation'] = owner_persist_error
                OwnerValidation.insert(apn, county, owner_error)

        if errors and fields:
            OwnerValidation.insert(apn, county, errors)

        return None

    def combine_mapped_to_csv_sample(self,
                                     file_generator,
                                     process_func,
                                     map_schema,
                                     output_file_name,
                                     queue_number,
                                     total_files):
        """
        To check whether we are mapping / validating correctly
        """
        output_file_name = output_file_name.name.split('.')[0]
        output_folder = DATA_IMPORT / 'output' / 'nassau' / 'assessment' / self.folder_name
        # create folder if does not exists
        output_folder.mkdir(parents=True, exist_ok=True)
        path = output_folder / f'{output_file_name}.csv'
        with open(path, 'w+') as f:
            w = csv.writer(f)
            lines = file_generator.readlines()
            with click.progressbar(
                    lines,
                    label=f'processing {queue_number}th out of {total_files}') as bar:
                for i, line in enumerate(bar):
                    # next_row = self.map_using_schema(
                    #     line, process_func(line), map_schema
                    # )
                    next_row = process_func(line)
                    # first write columns to file
                    if i == 0:
                        # w.writerow(next_row[0].keys())
                        w.writerow(next_row.keys())
                    # then write rest of the rows
                    # w.writerow(next_row[0].values())
                    w.writerow(next_row.values())
        return None

    def async_store_to_database(self, opened_file, process_func,
                                schema, input_file_size):
        schema = schema(unknown=EXCLUDE)
        with ThreadPoolExecutor(MAX_WORKER_COUNT) as executor:
            future_to_line = [
                executor.submit(self.map_using_schema, line,
                                process_func(line), schema, True)
                for line in opened_file.readlines()
            ]
            print('assessment futures submitted')
            with click.progressbar(
                    length=input_file_size,
                    label='nassau assessment') as bar:
                for future in as_completed(future_to_line):
                    try:
                        data, line = future.result()
                        bar.update(len(line))
                    except Exception as exc:
                        print(exc)

        # for line in opened_file.readlines():
        #     self.map_using_schema(line, process_func(line), schema, True)
        return None

    def process_input_file(self, file_name, queue_number, total_files,
                           write_to_csv=False,
                           persist=False):
        assessment_type = 400
        assert assessment_type in self.process_functions
        assert assessment_type in self.mapping_schemas
        process_func = self.process_functions.get(assessment_type)
        mapping_schema = self.mapping_schemas.get(assessment_type)
        input_file_size = file_name.stat().st_size
        with open(file_name) as f:
            if write_to_csv:
                self.combine_mapped_to_csv_sample(f,
                                                  process_func,
                                                  mapping_schema,
                                                  file_name,
                                                  queue_number,
                                                  total_files)
            if persist:
                self.async_store_to_database(f, process_func,
                                             mapping_schema,
                                             input_file_size)

    def remove_files(self, path):
        import os

        files = list(path.glob('*.csv'))

        for f in files:
            try:
                os.remove(f)
            except OSError as e:
                print(f"Error: {f} : {e.strerror}")

    def join_dataframes(self):
        """
        Join parsed result files to one .csv file and optional import to database
        """
        input_path = DATA_IMPORT / 'output' / 'nassau' / 'assessment' / self.folder_name
        self.remove_files(input_path)
        # process input folder get parsed assessment files in the output directory
        self.process_input_folder(write_to_csv=True, persist=False)

        folder_files = list(input_path.glob('*.csv'))

        frames = [pd.read_csv(f, low_memory=False, dtype={'parid': str}) for f in folder_files]
        df = pd.concat(frames)

        # remove useless columns
        df = df[['parid', 'swiss_code', 'village_1', 'village_1_pct', 'village_2', 'village_2_pct', 'village_3',
                 'village_3_pct', 'total_assessment']]

        return df

    def process_dir(self, operation: ProcessorOperation = ProcessorOperation.INSERT):
        df = self.join_dataframes()
        if self.to_file:
            output_path = DATA_IMPORT / 'output' / 'nassau' / 'assessment' / f'assessments_{self.folder_name}.csv'
            df.to_csv(output_path, index=False)

        if self.persist:
            table_name = f'nassau_assessments_{self.folder_name}'
            schema = 'data_source'
            self.import_data(df, table_name, schema)

            if operation == ProcessorOperation.INSERT:
                self.insert_data(table_name, schema, self.assessment_type_id, self.assessment_date_id)

            if self.drop_imported:
                self.drop_data(table_name, schema)

            # apply changes
            db.session.commit()

    def insert_data(self, table_name, schema, assessment_type_id, assessment_date_id):
        query = f'''
        INSERT INTO public.assessment
            (
                value, assessment_type, property_id, swiss_code, village_1, village_1_pct, village_2,
                village_2_pct, village_3, village_3_pct, assessment_id, override_value, assessment_value
            )
            (
            SELECT
                    ds.total_assessment,
                    {assessment_type_id},
                    (SELECT id FROM public.property WHERE apn = ds.parid),
                    ds.swiss_code,
                    ds.village_1,
                    ds.village_1_pct::double precision,
                    ds.village_2,
                    ds.village_2_pct::double precision,
                    ds.village_3,
                    ds.village_3_pct::double precision,
                    {assessment_date_id},
                    NULL,
                    ds.total_assessment
             FROM {schema}.{table_name} ds
                      JOIN public.property p ON ds.parid = p.apn
            );
        '''
        db.session.execute(query)
        print(f"Inserted data to '{table_name}'")

    def process_input_folder(self, write_to_csv, persist):
        """
        We are doing two step processing. First we slice data as per
        indices defined in FOIL_AADAPT_VS_Legacy_110801.xls documentation.
        Then we map and validate the data as per marshmallow schema.
        Final result we either display as csv sample or we can store
        to the database together with errors/warnings occur
        at the mapping stage.
        Mappers and Processors selected based on the file type.
        :return: mapped / validated table and/or stored errors
        together with mapped data to database.
         Depends on what function we invoke.
        """
        input_path = DATA_IMPORT / 'src' / 'nassau' / 'assessment' / self.folder_name

        folder_files = list(input_path.glob('*'))
        folder_non_empty_files = [
            file for file in folder_files
            if file.stat().st_size and '400' in file.name]
        total_files = len(folder_non_empty_files)
        for i, file in enumerate(folder_non_empty_files):
            file_name_suffix = file.name.split('.')[0][-3:]
            if file_name_suffix != '400':
                continue
            # if file.name != 'sample400.TXT':
            #     continue
            self.process_input_file(file,
                                    i,
                                    total_files,
                                    write_to_csv, persist)
        return None
