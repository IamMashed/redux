import glob
from collections import defaultdict
from pathlib import Path

import pandas as pd

from app.data_import.florida import commit_property, map_row, read_shp, execute_task, \
    GISProcessor, FloridaPropertyProcessor
from app.data_import.palmbeach.data_loading import append_row_to_csv, read_txt_file_as_chunks, CHUNK_SIZE
from app.database.models import Property
from app.database.models.property import PropertyValidation, PalmBeachParcelSchema, \
    PalmbeachLandSchema, PalmbeachCondoSchema, PalmbeachObySchema, PalmbeachResbldSchema, PalmbeachCombldSchema
from app.utils.comp_utils import is_whitelisted
from app.utils.fix_address import capitalize_address

PALMBEACH_HEATING_FUEL_TYPES = {
    1: 'NONE',
    2: 'OIL',
    3: 'GAS',
    4: 'ELECTRIC',
    5: 'SOLAR'
}

PALMBEACH_HEAT_SYSTEM_TYPES = {
    1: 'NONE',
    2: 'CONVECTION',
    3: 'FORCED / NO DUCT',
    4: 'FORCED AIR DUCT',
    5: 'HOT WATER',
    6: 'STEAM',
    7: 'RADIANT ELEC',
    8: 'RADIANT WATER',
    9: 'CHILLED WATER'
}

PALMBEACH_CONDITION_CODES = {
    0: 'NA',
    1: 'NO HTG/AC',
    2: 'AC ONLY',
    3: 'HTG & AC',
    4: 'HTG ONLY',
    5: 'NONE',
    6: 'PACKAGE UNITS',
    7: 'CENTRAL',
    8: 'CHILLED WATER'

}

PALMBEACH_FIREPLACE_CODES = {
    'FRP': 'Fireplace',
    'OFP': 'OUTDOOR FIREPLACE'
}

PALMBEACH_COMBLD_CONDITION_CODES = {
    0: None,
    1: 'PACKAGE UNITS',
    2: 'CENTRAL',
    3: 'CHILLED WATER'
}

PALMBEACH_BASEMENT_TYPES = {
    'BMT': 'BASEMENT'
}

PALMBEACH_GARAGE_TYPES = {
    'GAR': 'GARAGE'
}

PALMBEACH_PATIO_TYPES = {
    'PAT': 'PATIO'
}

PALMBEACH_PORCH_TYPES = {
    'FEP': 'FINISHED ENCL. PORCH',
    'FOP': 'FINISHED OPEN PORCH',
    'FSP': 'FIN SCREEN PORCH',
    'UEP': 'UNFIN ENCLOSED PORCH',
    'UOP': 'UNFIN OPEN PORCH'
}

PALMBEACH_POOL_TYPES = {
    'CPH': 'CABANA/POOL HOUSE',
    'POH': 'Poolhouse',
    'POL': 'POOL - IN-GROUND',
    'SPC': 'SWIMMING POOL COMMERCIAL'
}

PALMBEACH_DATA_COMPOSITE = {
    0: 'TOTAL_NUMBER_BLDG_RESIDENTIAL',
    1: 'TOTAL_NUMBER_BLDG_COMMERCIAL',
    2: 'TOTAL_NUMBER_LAND',
    3: 'TOTAL_NUMBER_OBY'
}


class PalmbeachPropertyProcessor(FloridaPropertyProcessor):

    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(PalmbeachPropertyProcessor, self).__init__(
            provider_name='palmbeach',
            persist=persist,
            to_file=to_file
        )
        self._file_name = file_name

    def process_row(self, row):
        # ignore rows contain *CONFIDENTIAL*
        if 'CONFIDENTIAL' in row:
            pass
        else:
            # parse a row
            parsed_row = self.parse_row(row)
            record_code = self._get_record_code(parsed_row)

            # do not store 'SALE'
            if record_code == 'SALE':
                pass
            # store 'OWNER' to csv in any case
            elif record_code == 'OWNER':
                self.append_to_csv(parsed_row)
            else:
                # store into db
                if self.persist:
                    self.commit_row(parsed_row)

                # save to .csv file
                if self.to_file:
                    self.append_to_csv(parsed_row)

    def process_input_file(self, parse_data: bool = True, insert_parcels: bool = True, update_parcels: bool = True,
                           update_parcels_land: bool = True):
        # create output directory
        self.output_dir().mkdir(parents=True, exist_ok=True)

        if parse_data:
            file_path = self.input_dir() / self.file_name
            (self.input_dir() / 'csv').mkdir(parents=True, exist_ok=True)

            print('start parsing')
            import time
            start_time = time.time()
            read_txt_file_as_chunks(file_path, chunk_size=CHUNK_SIZE, callback=self.process_lines)
            print(f'end parsing in {time.time() - start_time}')

        # commit all unique parcels
        if insert_parcels:
            self._file_name = Path(glob.glob(self.input_dir().as_posix() + "/PARCEL_PAS405*.csv")[0]).name
            parcels = pd.read_csv(self.input_dir() / self.file_name, low_memory=False, dtype=str)
            parcels.fillna('', inplace=True)
            execute_task(
                task=self.commit_parcel_row,
                iterator=parcels.iterrows(),
                total=len(parcels),
                desc=f'process {self.file_name}'
            )

        # update parcels inventories
        if update_parcels:
            # update parcels records with 'RESBLD', 'COMBLD', 'CONDO', 'OBY' data
            file_names = glob.glob((self.input_dir() / 'csv').as_posix() + "/*.csv")
            for i in range(len(file_names)):
                self._file_name = Path(file_names[i]).name
                df = pd.read_csv(self.input_dir() / 'csv' / self.file_name, low_memory=False, dtype=str)
                df.fillna('', inplace=True)

                execute_task(
                    task=self.update_parcel_row,
                    iterator=df.iterrows(),
                    total=len(df),
                    desc=f'update parcels from {self.file_name}, stage {i+1}/{len(file_names)}'
                )

        if update_parcels_land:
            self._file_name = 'LAND_PAS405_CERT2019_20191017.csv'
            df = pd.read_csv(self.input_dir() / self.file_name, low_memory=False, dtype=str)
            df.fillna('', inplace=True)

            execute_task(
                task=self.update_parcel_land_row,
                iterator=df.iterrows(),
                total=len(df),
                desc='update parcels land from {}'.format(self.file_name)
            )

    def update_parcel_land_row(self, row):
        record_code = self._get_record_code(row)
        line_number = self._get_line_number(row)

        if int(line_number) == 1:
            schema = self._get_record_schema()[record_code]
            mapped_row, errors = map_row(row.to_dict(), schema)

            from manage import app
            if self.persist:
                with app.app_context():
                    apn = mapped_row.get('apn')
                    county = mapped_row.get('county')

                    p = Property.query.filter_by(apn=apn, county=county).first()

                    if not p:
                        errors['property'] = f'property with apn {apn} not in database'
                    else:
                        # update parcels inventories , which has only lands
                        if p.gla_sqft is None:
                            update_error = Property.update_if_exists(mapped_row)

                            if update_error:
                                errors['database_operation'] = update_error

                        elif p.lot_size is None:
                            # update combld lot_size only from land
                            update_error = Property.update_if_exists(dict(
                                apn=apn,
                                county=county,
                                lot_size=mapped_row.get('lot_size')
                            ))

                            if update_error:
                                errors['database_operation'] = update_error
                        else:
                            print('NOT updating property with {}'.format(apn))

                    if errors:
                        PropertyValidation.insert(apn, county, errors)
            if self.to_file:
                append_row_to_csv(mapped_row, (self.output_dir() / (record_code + '.csv')).as_posix())

    def update_parcel_row(self, row):
        record_code = self._get_record_code(row)
        card_number = self._get_card_number(row)

        if card_number == '1':

            schema = self._get_record_schema()[record_code]
            mapped_row, errors = map_row(row.to_dict(), schema)

            if self.persist:

                from manage import app
                with app.app_context():
                    apn = mapped_row.get('apn')
                    county = mapped_row.get('county')

                    p = Property.query.filter_by(apn=apn, county=county).first()

                    if not p:
                        errors['property'] = f'property with apn {apn} not in database'
                    else:
                        update_error = Property.update_if_exists(mapped_row)

                        if update_error:
                            errors['database_operation'] = update_error

                    if errors:
                        PropertyValidation.insert(apn, county, errors)
            if self.to_file:
                append_row_to_csv(mapped_row, (self.output_dir() / (record_code + '.csv')).as_posix())

    def commit_parcel_row(self, row):
        record_code = self._get_record_code(row)

        schema = self._get_record_schema()[record_code]
        mapped_row, errors = map_row(row.to_dict(), schema)

        if self.persist:
            commit_property(mapped_row, errors)

        if self.to_file:
            append_row_to_csv(mapped_row, (self.output_dir() / (record_code + '.csv')).as_posix())

    def process_lines(self, data, eof):
        """ Callback function for file reading """

        # check if end of file reached
        if not eof:

            # ignore rows contain *CONFIDENTIAL*
            if 'CONFIDENTIAL' in data:
                pass

            else:
                # parse a row
                parsed_row = self.parse_row(data)

                input_file = parsed_row['RECORD_CODE'] + '_PAS405_CERT2019_20191017.TXT'
                if parsed_row['RECORD_CODE'] == 'SALE':
                    pass
                elif parsed_row['RECORD_CODE'] in ['OWNER', 'PARCEL', 'LAND']:
                    self.input_dir().mkdir(parents=True, exist_ok=True)
                    output_path = (self.input_dir() / input_file).as_posix()[:-4] + '.csv'
                    append_row_to_csv(parsed_row, output_path)
                else:
                    output_path = (self.input_dir() / 'csv' / input_file).as_posix()[:-4] + '.csv'
                    append_row_to_csv(parsed_row, output_path)
        else:
            pass

    def append_to_csv(self, row):
        self.output_dir().mkdir(parents=True, exist_ok=True)
        output_file = row['RECORD_CODE'] + '_PAS405_CERT2019_20191017.TXT'
        output_path = (self.output_dir() / output_file).as_posix()[:-4] + '.csv'
        append_row_to_csv(row, output_path)

    def parse_row(self, row):
        """
        Parse row values of the input data source file

        :param row: The row of file reader
        :return: dictionary of {column_name: value}
        """
        data = dict()

        data['FILE_KEY'] = row[0:23].strip()
        data['PROPERTY_CONTROL_NUMBER'] = row[0:17].strip()
        data['CITY'] = row[0:2].strip()
        data['RANGE'] = row[2:4].strip()
        data['TOWNSHIP'] = row[4:6].strip()
        data['SECTION'] = row[6:8].strip()
        data['SUBDIVISION'] = row[8:10].strip()
        data['BLOCK'] = row[10:13].strip()
        data['LOT'] = row[13:17].strip()
        data['RECORD_CODE'] = row[17:23].strip()

        # according to the provided layout parse row and update data
        data.update(self.record_code_map()[data['RECORD_CODE']](row))

        data['apn'] = data['PROPERTY_CONTROL_NUMBER']
        data['county'] = self.provider_name
        data['section'] = data['SECTION']
        data['block'] = data['BLOCK']
        data['lot'] = data['LOT']
        data['city'] = capitalize_address(data['CITY'])
        data['state'] = 'FL'
        data['is_residential'] = is_whitelisted(**data)

        return data

    @classmethod
    def record_code_map(cls):
        return {
            "CONDO": cls._parse_condo,
            "LAND": cls._parse_land,
            "OBY": cls._parse_oby,
            "OWNER": cls._parse_owner,
            "PARCEL": cls._parse_parcel,
            "RESBLD": cls._parse_resbld,
            "SALE": cls._parse_sale,
            "COMBLD": cls._parse_combld,
        }

    @classmethod
    def _parse_parcel(cls, row):
        data = dict()

        data['SITUS_ADDRESS'] = row[23:154].strip()
        data['SITUS_ADDRESS_PREFIX'] = row[23:25].strip()
        data['SITUS_ADDRESS_NUMBER'] = row[25:35].strip()
        data['SITUS_ADDRESS_ADDITIONAL'] = row[35:41].strip()
        data['SITUS_ADDRESS_PRE_DIRECTIONAL'] = row[41:43].strip()
        data['SITUS_ADDRESS_STREET_NAME'] = row[43:73].strip()
        data['SITUS_ADDRESS_STREET_SUFFIX'] = row[73:81].strip()
        data['SITUS_ADDRESS_STREET_SUFFIX2'] = row[81:89].strip()
        data['SITUS_ADDRESS_CITY_NAME'] = row[89:129].strip()
        data['SITUS_ADDRESS_UNIT_DESCRIPTION'] = row[129:139].strip()
        data['SITUS_ADDRESS_UNIT_NUMBER'] = row[139:149].strip()
        data['SITUS_ADDRESS_ZIP_CODE'] = row[149:154].strip()

        data['LAND_USE_CODE'] = row[154:158].strip()
        data['LAND_USE_DESCRIPTION'] = row[158:173].strip()
        data['TOTAL_MARKET_VALUE'] = row[173:186].strip()
        data['TOTAL_NON-SCHOOL_ASSESSED_VALUE'] = row[186:199].strip()
        data['TOTAL_CLASS_USE_VALUE'] = row[199:212].strip()
        data['TOTAL_IMPROVEMENT_VALUE'] = row[212:225].strip()
        data['TOTAL_LAND_VALUE'] = row[225:238].strip()
        data['TOTAL_MARKET_VALUE_FOR_AG'] = row[238:251].strip()
        data['TOTAL_PREVIOUS_MARKET_VALUE'] = row[251:264].strip()
        data['TOTAL_NUMBER_BLDG_RESIDENTIAL'] = row[265:268].strip()
        data['TOTAL_NUMBER_BLDG_COMMERCIAL'] = row[269:272].strip()
        data['TOTAL_NUMBER_LAND'] = row[273:276].strip()
        data['TOTAL_NUMBER_OBY'] = row[277:280].strip()

        data['data_composite'] = [
            data['TOTAL_NUMBER_BLDG_RESIDENTIAL'],
            data['TOTAL_NUMBER_BLDG_COMMERCIAL'],
            data['TOTAL_NUMBER_LAND'],
            data['TOTAL_NUMBER_OBY']
        ]

        data['number'] = cls._parse_number(data['SITUS_ADDRESS_NUMBER'])
        data['street'] = capitalize_address(cls._parse_street(data['SITUS_ADDRESS_STREET_NAME']))
        data['address'] = capitalize_address(cls._parse_address(data['SITUS_ADDRESS']))
        data['zip'] = cls._parse_zip_code(data.get('SITUS_ADDRESS_ZIP_CODE'))
        data['property_class'] = data.get('LAND_USE_CODE')

        return data

    @classmethod
    def _valid(cls, value):
        if value is None or value == '':
            return False
        return True

    @classmethod
    def _parse_address(cls, value):
        new_value = ' '.join(value.split())
        return new_value.strip()

    @classmethod
    def _parse_number(cls, value):
        new_value = ' '.join(value.split())
        return new_value.strip()

    @classmethod
    def _parse_street(cls, value):
        new_value = ' '.join(value.split())
        return new_value.strip()

    @classmethod
    def _parse_full_baths(cls, value):
        if not cls._valid(value):
            return None
        try:
            return int(float(value))
        except ValueError:
            return None

    @classmethod
    def _parse_half_baths(cls, value):
        if not cls._valid(value):
            return None
        try:
            return int(float(value))
        except ValueError:
            return None

    @classmethod
    def _parse_bedrooms(cls, value):
        if not cls._valid(value):
            return None
        try:
            return int(float(value))
        except ValueError:
            return None

    @classmethod
    def _parse_story_height(cls, value):
        if not cls._valid(value):
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @classmethod
    def _parse_card_number(cls, value):
        if not cls._valid(value):
            return None
        try:
            return int(value)
        except ValueError:
            return None

    @classmethod
    def _parse_condition_type(cls, value):
        if not cls._valid(value):
            return None

        for k, v in PALMBEACH_CONDITION_CODES.items():
            if v == value:
                return k
        return None

    @classmethod
    def _parse_heat_type(cls, value):
        if not cls._valid(value):
            return 1

        for k, v in PALMBEACH_HEAT_SYSTEM_TYPES.items():
            if v == value:
                return k
        return 1

    @classmethod
    def _parse_owner(cls, row):
        data = dict()

        data['OWNER_NAME'] = row[23:63].strip()
        data['OWNER_ADDRESS_LINE_1'] = row[63:113].strip()
        data['OWNER_ADDRESS_LINE_2'] = row[113:163].strip()
        data['OWNER_ADDRESS_LINE_3'] = row[163:213].strip()
        data['LEGAL_LINE_1'] = row[213:273].strip()
        data['LEGAL_LINE_2'] = row[273:333].strip()
        data['LEGAL_LINE_3'] = row[333:393].strip()

        return data

    @classmethod
    def _parse_resbld(cls, row):
        data = dict()

        data['BUILDING_CARD_NUMBER'] = row[23:27].strip()
        data['CLASSIFICATION'] = row[27:31].strip()
        data['CLASSIFICATION_DESCRIPTION'] = row[31:46].strip()
        data['YEAR_BUILT'] = row[46:50].strip()
        data['EFFECTIVE_YEAR'] = row[50:54].strip()
        data['NUMBER_OF_BEDROOMS'] = row[54:56].strip()
        data['NUMBER_OF_FULL_BATHROOMS'] = row[56:58].strip()
        data['NUMBER_OF_HALF_BATHROOMS'] = row[58:60].strip()
        data['STORY_HEIGHT'] = row[60:64].strip()
        data['EXTERIOR_WALL_CODE'] = row[64:66].strip()
        data['EXTERIOR_WALL_DESCRIPTION'] = row[66:91].strip()
        data['EXTERIOR_WALL2_CODE'] = row[91:93].strip()
        data['EXTERIOR_WALL2_DESCRIPTION'] = row[93:108].strip()
        data['ROOF_STRUCTURE_CODE'] = row[108:110].strip()
        data['ROOF_STRUCTURE_DESCRIPTION'] = row[110:125].strip()
        data['ROOF_COVER_CODE'] = row[125:127].strip()
        data['ROOF_COVER_DESCRIPTION'] = row[127:142].strip()
        data['INTERIOR_WALL_CODE'] = row[142:144].strip()
        data['INTERIOR_WALL_DESCRIPTION'] = row[144:159].strip()
        data['INTERIOR_WALL2_CODE'] = row[159:161].strip()
        data['INTERIOR_WALL2_DESCRIPTION'] = row[161:176].strip()
        data['FLOOR_TYPE_1_CODE'] = row[176:178].strip()
        data['FLOOR_TYPE_1_DESCRIPTION'] = row[178:193].strip()
        data['FLOOR_TYPE_2_CODE'] = row[193:195].strip()
        data['FLOOR_TYPE_2_DESCRIPTION'] = row[195:210].strip()
        data['HEAT_CODE'] = row[210:211].strip()
        data['HEAT_DESCRIPTION'] = row[211:226].strip()
        data['HEATING_SYSTEM_TYPE'] = row[226:227].strip()
        data['HEATING_SYSTEM_TYPE_DESCRIPTION'] = row[227:242].strip()
        data['HEATING_FUEL_TYPE'] = row[242:243].strip()
        data['HEATING_FUEL_TYPE_DESCRIPTION'] = row[243:258].strip()
        data['GRADE_CODE'] = row[258:261].strip()
        data['GRADE_DESCRIPTION'] = row[261:276].strip()
        data['CONDITION'] = row[276:278].strip()
        data['CONDITION_DESCRIPTION'] = row[278:293].strip()
        data['ADJUSTMENT_FACTOR'] = row[294:301].strip()
        data['BUILDING_VALUE'] = row[302:312].strip()
        data['BUILDING_AREA'] = row[313:323].strip()
        data['TOTAL_AREA'] = row[324:334].strip()
        data['SQUARE_FOOT_LIVING_AREA'] = row[335:345].strip()

        data['is_condo'] = cls._parse_is_condo(data.get('CLASSIFICATION'))
        data['building_code'] = cls._parse_building_code(data.get('CLASSIFICATION'))
        data['full_baths'] = cls._parse_full_baths(data.get('NUMBER_OF_FULL_BATHROOMS'))
        data['half_baths'] = cls._parse_half_baths(data.get('NUMBER_OF_HALF_BATHROOMS'))
        data['bedrooms'] = cls._parse_bedrooms(data.get('NUMBER_OF_BEDROOMS'))
        data['story_height'] = cls._parse_story_height(data.get('STORY_HEIGHT'))
        data['lot_size'] = data.get('TOTAL_AREA')
        data['gla_sqft'] = data.get('SQUARE_FOOT_LIVING_AREA')
        data['gas'] = True if data.get('HEATING_FUEL_TYPE', 0) == '3' else False
        data['condition'] = cls._parse_condition_type(data['HEAT_DESCRIPTION'])
        data['heat_type'] = cls._parse_heat_type(data['HEATING_SYSTEM_TYPE_DESCRIPTION'])
        data['age'] = data['YEAR_BUILT']
        data['card_number'] = cls._parse_card_number(data['BUILDING_CARD_NUMBER'])

        return data

    @classmethod
    def _parse_combld(cls, row):
        data = dict()

        data['BUILDING_CARD_NUMBER'] = row[23:27].strip()
        data['STRUCTURE_CODE'] = row[27:30].strip()
        data['STRUCTURE_DESCRIPTION'] = row[30:45].strip()
        data['YEAR_BUILT'] = row[45:49].strip()
        data['EFFECTIVE_YEAR'] = row[49:53].strip()
        data['NUMBER_OF_UNITS'] = row[53:57].strip()
        data['STORIES'] = row[57:59].strip()
        data['EXTERIOR_WALL_CODE'] = row[59:61].strip()
        data['EXTERIOR_WALL_DESCRIPTION'] = row[61:76].strip()
        data['INTERIOR_FINISH_CODE'] = row[76:77].strip()
        data['INTERIOR_FINISH_DESCRIPTION'] = row[77:92].strip()
        data['CONSTRUCTION_TYPE'] = row[92:94].strip()
        data['CONSTRUCTION_TYPE_DESCRIPTION'] = row[94:109].strip()
        data['AIR_CONDITIONING_CODE'] = row[109:110].strip()
        data['AIR_CONDITIONING_DESCRIPTION'] = row[110:125].strip()
        data['GRADE_CODE'] = row[125:128].strip()
        data['GRADE_DESCRIPTION'] = row[128:143].strip()
        data['FUNCTIONAL_UTILITY_CODE'] = row[143:144].strip()
        data['ADJUSTMENT_FACTOR'] = row[145:152].strip()
        data['BUILDING_VALUE'] = row[153:163].strip()
        data['BUILDING_AREA'] = row[164:174].strip()

        data['gla_sqft'] = data.get('BUILDING_AREA')
        data['condition'] = cls._parse_condition_type(data['AIR_CONDITIONING_DESCRIPTION'])
        data['age'] = data['YEAR_BUILT']
        data['card_number'] = cls._parse_card_number(data['BUILDING_CARD_NUMBER'])

        return data

    @classmethod
    def _parse_condo(cls, row):
        data = dict()

        data['COMPLEX_ID'] = row[23:33].strip()
        data['COMPLEX_NAME'] = row[33:93].strip()
        data['UNIT_NUMBER'] = row[93:103].strip()
        data['BUILDING_CARD'] = row[103:107].strip()
        data['CLASSIFICATION_CODE'] = row[107:111].strip()
        data['CLASSIFICATION_DESCRIPTION'] = row[111:125].strip()
        data['YEAR_BUILT'] = row[126:130].strip()

        data['CONDOMINIUM_FLOOR_TYPE_CODE'] = row[130:134].strip()
        data['CONDOMINIUM_FLOOR_TYPE_DESCRIPTION'] = row[134:154].strip()
        data['CONDOMINIUM_FLOOR_LEVEL'] = row[155:157].strip()
        data['NUMBER_OF_BEDROOMS'] = row[158:160].strip()
        data['NUMBER_OF_BATHROOMS'] = row[161:165].strip()
        data['AREA'] = row[166:172].strip()
        data['VALUE'] = row[173:183].strip()
        data['NUMBER_OF_HALF_BATHS'] = row[184:187].strip()

        data['is_condo'] = cls._parse_is_condo(data.get('CLASSIFICATION_CODE'))
        data['building_code'] = cls._parse_building_code(data.get('CLASSIFICATION_CODE'))
        data['full_baths'] = cls._parse_full_baths(data.get('NUMBER_OF_BATHROOMS'))
        data['half_baths'] = cls._parse_half_baths(data.get('NUMBER_OF_HALF_BATHS'))
        data['bedrooms'] = cls._parse_bedrooms(data.get('NUMBER_OF_BEDROOMS'))
        data['gla_sqft'] = data.get('AREA')
        data['age'] = data['YEAR_BUILT']
        data['card_number'] = cls._parse_card_number(data['BUILDING_CARD'])

        return data

    @classmethod
    def _parse_sale(cls, row):
        data = dict()

        data['SALES_BOOK_1'] = row[23:28].strip()
        data['SALES_PAGE_1'] = row[28:32].strip()
        data['SALES_DATE_1'] = row[32:41].strip()
        data['SALES_INSTRUMENT_TYPE_1'] = row[41:43].strip()
        data['SALES_VALIDITY_CODE_1'] = row[43:45].strip()
        data['SALES_TYPE_CODE_1'] = row[45:46].strip()
        data['SALES_PRICE_1'] = row[47:57].strip()
        data['SALES_BOOK_2'] = row[66:71].strip()
        data['SALES_PAGE_2'] = row[71:75].strip()
        data['SALES_DATE_2'] = row[75:84].strip()
        data['SALES_INSTRUMENT_TYPE_2'] = row[84:86].strip()
        data['SALES_VALIDITY_CODE_2'] = row[86:88].strip()
        data['SALES_TYPE_CODE_2'] = row[88:89].strip()
        data['SALES_PRICE_2'] = row[90:100].strip()
        data['SALES_BOOK_3'] = row[109:114].strip()
        data['SALES_PAGE_3'] = row[114:118].strip()
        data['SALES_DATE_3'] = row[118:127].strip()
        data['SALES_INSTRUMENT_TYPE_3'] = row[127:129].strip()
        data['SALES_VALIDITY_CODE_3'] = row[129:131].strip()
        data['SALES_TYPE_CODE_3'] = row[131:132].strip()
        data['SALES_PRICE_3'] = row[133:143].strip()
        data['SALES_BOOK_4'] = row[152:157].strip()
        data['SALES_PAGE_4'] = row[157:161].strip()
        data['SALES_DATE_4'] = row[161:170].strip()
        data['SALES_INSTRUMENT_TYPE_4'] = row[170:172].strip()
        data['SALES_VALIDITY_CODE_4'] = row[172:174].strip()
        data['SALES_TYPE_CODE_4'] = row[174:175].strip()
        data['SALES_PRICE_4'] = row[176:186].strip()
        data['SALES_BOOK_5'] = row[195:200].strip()
        data['SALES_PAGE_5'] = row[200:204].strip()
        data['SALES_DATE_5'] = row[204:213].strip()
        data['SALES_INSTRUMENT_TYPE_5'] = row[213:215].strip()
        data['SALES_VALIDITY_CODE_5'] = row[215:217].strip()
        data['SALES_TYPE_CODE_5'] = row[217:218].strip()
        data['SALES_PRICE_5'] = row[219:229].strip()

        return data

    @classmethod
    def _parse_oby(cls, row):
        data = dict()

        data['BUILDING_CARD_NUMBER'] = row[23:27].strip()
        data['LINE_NUMBER'] = row[27:31].strip()
        data['TYPE_CODE'] = row[31:34].strip()
        data['TYPE_CODE_DESCRIPTION'] = row[34:64].strip()
        data['MEASUREMENT_1'] = row[65:69].strip()
        data['MEASUREMENT_2'] = row[70:74].strip()
        data['UNITS'] = row[75:78].strip()
        data['RATE'] = row[79:92].strip()
        data['AREA'] = row[92:101].strip()
        data['YEAR_BUILT'] = row[101:105].strip()
        data['MKTADJ'] = row[106:109].strip()
        data['ADJRCNLD'] = row[110:120].strip()

        data['fireplaces'] = 1 if data.get('TYPE_CODE', '') in PALMBEACH_FIREPLACE_CODES.keys() else 0
        data['garages'] = 1 if data.get('TYPE_CODE', '') == 'GAR' else 0
        data['pool'] = True if data.get('TYPE_CODE', '') in ['CPH', 'POH', 'POL', 'SPC'] else False

        data['garage_type'] = cls._parse_garage_type(data.get('TYPE_CODE'))
        data['basement_type'] = cls._parse_basement_type(data.get('TYPE_CODE'))
        data['patio_type'] = cls._parse_patio_type(data.get('TYPE_CODE'))
        data['porch_type'] = cls._parse_porch_type(data.get('TYPE_CODE'))
        data['card_number'] = cls._parse_card_number(data['BUILDING_CARD_NUMBER'])

        return data

    @classmethod
    def _parse_land(cls, row):
        data = dict()

        data['LINE_NUMBER'] = row[23:27].strip()
        data['LAND_TYPE_CODE'] = row[27:28].strip()
        data['LAND_TYPE_DESCRIPTION'] = row[28:43].strip()
        data['CODE'] = row[43:46].strip()
        data['CODE_DESCRIPTION'] = row[46:61].strip()
        data['CLASSIFICATION_CODE'] = row[61:65].strip()
        data['CLASSIFICATION_DESCRIPTION'] = row[65:85].strip()
        data['ZONE'] = row[85:94].strip()
        data['ACTUAL_FRONTAGE_TYPE_F'] = row[94:99].strip()
        data['EFFECTIVE_FRONTAGE'] = row[100:104].strip()
        data['DEPTH'] = row[105:109].strip()
        data['NOTE1'] = row[109:149].strip()
        data['SQUARE_FEET'] = row[150:160].strip()
        data['ACRES'] = row[161:174].strip()
        data['UNITS'] = row[175:182].strip()
        data['BASE_RATE'] = row[183:192].strip()
        data['OVERRIDE_INCREMENTAL_RATE'] = row[193:203].strip()
        data['PRICE'] = row[204:214].strip()
        data['AG_FLAG'] = row[214:215].strip()
        data['is_condo'] = cls._parse_is_condo(data.get('CLASSIFICATION_CODE'))
        data['building_code'] = cls._parse_building_code(data.get('CLASSIFICATION_CODE'))

        data['lot_size'] = data.get('ACRES')
        data['gla_sqft'] = data.get('SQUARE_FEET')

        return data

    @staticmethod
    def _parse_patio_type(value):
        if value in PALMBEACH_PATIO_TYPES.keys():
            return tuple(PALMBEACH_PATIO_TYPES.keys()).index(value) + 1

        return 0

    @staticmethod
    def _parse_porch_type(value):
        if value in PALMBEACH_PORCH_TYPES.keys():
            return tuple(PALMBEACH_PORCH_TYPES.keys()).index(value) + 1

        return 0

    @staticmethod
    def _parse_basement_type(value):
        if value in PALMBEACH_BASEMENT_TYPES.keys():
            return tuple(PALMBEACH_BASEMENT_TYPES.keys()).index(value)

        return None

    @staticmethod
    def _parse_garage_type(value):
        if value in PALMBEACH_GARAGE_TYPES.keys():
            return tuple(PALMBEACH_GARAGE_TYPES.keys()).index(value)

        return None

    @classmethod
    def _parse_zip_code(cls, value):
        if value is None or value == '':
            return None
        try:
            return int(float(value))
        except ValueError:
            return None

    @classmethod
    def _parse_building_code(cls, value):
        if value is None or value == '':
            return None
        try:
            return int(value)
        except ValueError:
            return None

    @classmethod
    def _parse_is_condo(cls, value):
        try:
            if int(value) in [0, 40, 50, 400, 460, 1000, 1004, 1049, 1100, 1104, 1200, 1204, 1304, 1404, 1604, 1704,
                              1804, 1904, 2004, 2014, 2104, 2204, 2304, 2704, 3904, 4004, 4104, 4804, 4960, 4969, 8504]:
                return True
            return False
        except ValueError:
            return None

    @classmethod
    def sum_inventory_values(cls, x, y, keys_to_sum=None):
        if keys_to_sum is None:
            keys_to_sum = ['bedrooms', 'full_baths', 'half_baths', 'gla_sqft', 'lot_size', 'garages', 'fireplaces']

        ret = defaultdict(int)
        for d in [x, y]:
            for k, v in d.items():
                if (k in keys_to_sum) and (v is not None):
                    ret[k] += v

        return dict(ret)

    @classmethod
    def _get_record_code(cls, data):
        return data.get('RECORD_CODE')

    @classmethod
    def _get_card_number(cls, data):
        return data.get('card_number', None)

    @classmethod
    def _get_line_number(cls, data):
        return data.get('LINE_NUMBER', None)

    @classmethod
    def _get_record_schema(cls):
        return {
            "CONDO": PalmbeachCondoSchema,
            "LAND": PalmbeachLandSchema,
            "OBY": PalmbeachObySchema,
            "PARCEL": PalmBeachParcelSchema,
            "RESBLD": PalmbeachResbldSchema,
            "COMBLD": PalmbeachCombldSchema,
        }

    def commit_row(self, row):
        """
        Persist row into database.

        The row with the new 'apn' write into db.
        The row with the existing 'apn' update in the db

        :param row: parsed row
        """
        schema = self._get_record_schema()[self._get_record_code(row)]
        mapped_row, errors = map_row(row, schema)

        if errors is None:
            errors = dict()

        apn = mapped_row.get('apn')
        county = mapped_row.get('county')

        # insert new or update property
        from manage import app
        with app.app_context():
            p = Property.query.filter_by(apn=apn, county=county).first()

            if not p:
                # add new property to database
                commit_property(mapped_row, errors)
            else:
                fields_sum = self.sum_inventory_values(mapped_row, p.__dict__)
                update_error = Property.update_if_exists({**mapped_row, **fields_sum})

                if update_error:
                    errors['database_operation'] = update_error

            if errors:
                PropertyValidation.insert(apn, county, errors)


class PalmbeachGISProcessor(GISProcessor):
    def __init__(self, file_name: str, persist: bool, to_file: bool):
        super(PalmbeachGISProcessor, self).__init__(
            provider_name='palmbeach',
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

        parsed_row['apn'] = row.PARID
        parsed_row['county'] = self.provider_name
        parsed_row.update(self.parse_polygon_coordinates(row))

        return parsed_row
