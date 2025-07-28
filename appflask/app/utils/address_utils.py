import pandas as pd
from scourgify.normalize import normalize_addr_str
from sqlalchemy import create_engine

from app import db
from app.utils.constants import County
from config import DATA_IMPORT, SQLALCHEMY_DATABASE_URI

STREET_TYPE_ABBREVIATIONS = {
    'ALLEY': 'ALY',
    'ANNEX': 'ANX',
    'ARCADE': 'ARC',
    'AVENUE': 'AVE',
    'BAYOU': 'BYU',
    'BEACH': 'BCH',
    'BEND': 'BND',
    'BLUFF': 'BLF',
    'BLUFFS': 'BLFS',
    'BOTTOM': 'BTM',
    'BOULEVARD': 'BLVD',
    'BRANCH': 'BR',
    'BRIDGE': 'BRG',
    'BROOK': 'BRK',
    'BROOKS': 'BRKSV',
    'BURG': 'BG',
    'BURGS': 'BGS',
    'BYPASS': 'BYP',
    'CAMP': 'CP',
    'CANYON': 'CYN',
    'CAPE': 'CPE',
    'CAUSEWAY': 'CSWY',
    'CENTER': 'CTR',
    'CENTERS': 'CTRS',
    'CIRCLE': 'CIR',
    'CIRCLES': 'CIRS',
    'CLIFF': 'CLF',
    'CLIFFS': 'CLFS',
    'CLUB': 'CLB',
    'COMMON': 'CMN',
    'COMMONS': 'CMNS',
    'CONCOURSE': 'CONC',
    'CORNER': 'COR',
    'CORNERS': 'CORS',
    'COURSE': 'CRSE',
    'COURT': 'CT',
    'COURTS': 'CTS',
    'COVE': 'CV',
    'COVES': 'CVS',
    'CREEK': 'CRK',
    'CRESCENT': 'CRES',
    'CREST': 'CRST',
    'CROSSING': 'XING',
    'CROSSROAD': 'XRD',
    'CROSSROADS': 'XRDS',
    'CURVE': 'CURV',
    'DALE': 'DL',
    'DAM': 'DM',
    'DIVIDE': 'DV',
    'DRIVE': 'DR',
    'DRIVES': 'DRS',
    'ESTATE': 'EST',
    'ESTATES': 'ESTS',
    'EXPRESSWAY': 'EXPY',
    'EXTENSION': 'EXT',
    'EXTENSIONS': 'EXTS',
    'FALL': 'FALL',
    'FALLS': 'FL',
    'FERRY': 'FRY',
    'FIELD': 'FLD',
    'FIELDS': 'FLDS',
    'FLAT': 'FLT',
    'FLATS': 'FLTS',
    'FORD': 'FRD',
    'FORDS': 'FRDS',
    'FOREST': 'FRST',
    'FORGE': 'FRG',
    'FORGES': 'FRGS',
    'FORK': 'FRK',
    'FORKS': 'FRKS',
    'FORT': 'FT',
    'FREEWAY': 'FWY',
    'GARDEN': 'GDN',
    'GARDENS': 'GDNS',
    'GATEWAY': 'GTWY',
    'GLEN': 'GLN',
    'GLENS': 'GLNS',
    'GREEN': 'GRN',
    'GREENS': 'GRNS',
    'GROVE': 'GRV',
    'GROVES': 'GRVS',
    'HARBOR': 'HBR',
    'HARBORS': 'HBRS',
    'HAVEN': 'HVN',
    'HEIGHTS': 'HTS',
    'HIGHWAY': 'HWY',
    'HILL': 'HL',
    'HILLS': 'HLS',
    'HOLLOW': 'HOLW',
    'INLET': 'INLT',
    'ISLAND': 'IS',
    'ISLANDS': 'ISS',
    'ISLE': 'ISLE',
    'JUNCTION': 'JCT',
    'JUNCTIONS': 'JCTS',
    'KEY': 'KY',
    'KEYS': 'KYS',
    'KNOLL': 'KNL',
    'KNOLLS': 'KNLS',
    'LAKE': 'LK',
    'LAKES': 'LKS',
    'LAND': 'LAND',
    'LANDING': 'LNDG',
    'LANE': 'LN',
    'LIGHT': 'LGT',
    'LIGHTS': 'LGTS',
    'LOAF': 'LF',
    'LOCK': 'LCK',
    'LOCKS': 'LCKS',
    'LODGE': 'LDG',
    'LOOP': 'LOOP',
    'MALL': 'MALL',
    'MANOR': 'MNR',
    'MANORS': 'MNRS',
    'MEADOW': 'MDW',
    'MEADOWS': 'MDWS',
    'MEWS': 'MEWS',
    'MILL': 'ML',
    'MILLS': 'MLS',
    'MISSION': 'MSN',
    'MOTORWAY': 'MTWY',
    'MOUNT': 'MT',
    'MOUNTAIN': 'MTN',
    'MOUNTAINS': 'MTNS',
    'NECK': 'NCK',
    'ORCHARD': 'ORCH',
    'OVAL': 'OVAL',
    'OVERPASS': 'OPAS',
    'PARK': 'PARK',
    'PARKS': 'PARK',
    'PARKWAY': 'PKWY',
    'PARKWAYS': 'PKWY',
    'PASS': 'PASS',
    'PASSAGE': 'PSGE',
    'PATH': 'PATH',
    'PIKE': 'PIKE',
    'PINE': 'PNE',
    'PINES': 'PNES',
    'PLACE': 'PL',
    'PLAIN': 'PLN',
    'PLAINS': 'PLNS',
    'PLAZA': 'PLZ',
    'POINT': 'PT',
    'POINTS': 'PTS',
    'PORT': 'PRT',
    'PORTS': 'PRTS',
    'PRAIRIE': 'PR',
    'RADIAL': 'RADL',
    'RAMP': 'RAMP',
    'RANCH': 'RNCH',
    'RAPID': 'RPD',
    'RAPIDS': 'RPDS',
    'REST': 'RST',
    'RIDGE': 'RDG',
    'RIDGES': 'RDGS',
    'RIVER': 'RIV',
    'ROAD': 'RD',
    'ROADS': 'RDS',
    'ROUTE': 'RTE',
    'ROW': 'ROW',
    'RUE': 'RUE',
    'RUN': 'RUN',
    'SHOAL': 'SHL',
    'SHOALS': 'SHLS',
    'SHORE': 'SHR',
    'SHORES': 'SHRS',
    'SKYWAY': 'SKWY',
    'SPRING': 'SPG',
    'SPRINGS': 'SPGS',
    'SPUR': 'SPUR',
    'SPURS': 'SPUR',
    'SQUARE': 'SQ',
    'SQUARES': 'SQS',
    'STATION': 'STA',
    'STRAVENUE': 'STRA',
    'STREAM': 'STRM',
    'STREET': 'ST',
    'STREETS': 'STS',
    'SUMMIT': 'SMT',
    'TERRACE': 'TER',
    'THROUGHWAY': 'TRWY',
    'TRACE': 'TRCE',
    'TRACK': 'TRAK',
    'TRAFFICWAY': 'TRFY',
    'TRAIL': 'TRL',
    'TRAILER': 'TRLR',
    'TUNNEL': 'TUNL',
    'TURNPIKE': 'TPKE',
    'UNDERPASS': 'UPAS',
    'UNION': 'UN',
    'UNIONS': 'UNS',
    'VALLEY': 'VLY',
    'VALLEYS': 'VLYS',
    'VIADUCT': 'VIA',
    'VIEW': 'VW',
    'VIEWS': 'VWS',
    'VILLAGE VILL': 'VLG',
    'VILLAGES': 'VLGS',
    'VILLE': 'VL',
    'VISTA': 'VIS',
    'WALK': 'WALK',
    'WALKS': 'WALK',
    'WALL': 'WALL',
    'WAY': 'WAY',
    'WAYS': 'WAYS',
    'WELL': 'WL',
    'WELLS': 'WLS',
}


class AddressUnitParser(object):

    def __init__(self, county):
        self.county = county
        self.file_name = self._get_file_name(county)

    def _get_file_name(self, county):
        if county == County.PALMBEACH:
            return 'NAL60F201902.csv'
        elif county == County.MIAMIDADE:
            return 'NAL23F201901.csv'
        elif county == County.BROWARD:
            return 'NAL16F201901.csv'
        else:
            raise ValueError('Invalid county name')

    def normalize_street_type_abbreviations(self, address_string):
        address_splits = address_string.split(' ')
        if address_splits and len(address_splits) > 2:
            if address_splits[-2] in STREET_TYPE_ABBREVIATIONS.values():
                line2 = 'UNIT {}'.format(str(address_splits.pop(-1)))
                line1 = ' '.join(address_splits)
            else:
                line1 = address_string
                line2 = None
        else:
            line1 = address_string
            line2 = None

        address_parts = {
            'address_line_1': line1,
            'address_line_2': line2,
            'error': None
        }

        return address_parts

    def parse_county(self):
        """
        Parse NAL assessment county file. Column 'PHY_ADDR1' contain address line with units.
        Break 'PHY_ADDR1' into two parts: address line1, address line1 and override 'PHY_ADDR1', 'PHY_ADDR2'
        Return .csv file with updated address lines
        """
        output_dir = DATA_IMPORT / 'output' / self.county / 'property'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'parsed_{self.county}_address_line.csv'

        df = pd.read_csv(
            DATA_IMPORT / 'src' / self.county / 'assessment' / self.file_name,
            low_memory=False,
            usecols=['PARCEL_ID', 'PHY_ADDR1', 'PHY_ADDR2', 'DOR_UC'],
            dtype=str
        )
        df = df[~df.PHY_ADDR1.isna()].reset_index()
        # df['DOR_UC'].astype(int)
        # df = df[df.DOR_UC == '004'].copy().reset_index()
        df['error'] = ''

        total = len(df)
        import time
        start = time.time()
        for index, row in df.iterrows():
            address_string = row['PHY_ADDR1']
            splits = address_string.split(' ')

            # do not parse if the last part of the address is a street type full name or street type abbreviation
            if splits and len(splits) > 1 and (splits[-1] in STREET_TYPE_ABBREVIATIONS.values() or
                                               STREET_TYPE_ABBREVIATIONS.get(splits[-1])):
                continue
            print(f'{index} of {total}')
            try:
                # check if before last element is street type abbreviation
                addr_parsed = self.normalize_street_type_abbreviations(address_string)
                if not addr_parsed['address_line_2']:
                    # use 'us address' lib to parse the address
                    addr_parsed = normalize_addr_str(address_string)

                    # if not valid
                    if addr_parsed['address_line_2'] and len(addr_parsed['address_line_2'].split(' ')) > 2:
                        addr_parsed['address_line_1'] = address_string
                        addr_parsed['address_line_2'] = None
                    else:
                        df['PHY_ADDR1'][index] = addr_parsed['address_line_1']
                        df['PHY_ADDR2'][index] = addr_parsed['address_line_2']
                        df['error'][index] = addr_parsed.get('error', None)
                else:
                    df['PHY_ADDR1'][index] = addr_parsed['address_line_1']
                    df['PHY_ADDR2'][index] = addr_parsed['address_line_2']
                    df['error'][index] = addr_parsed.get('error', None)
            except Exception as e:
                df['PHY_ADDR1'][index] = address_string
                df['PHY_ADDR2'][index] = None
                df['error'][index] = str(e)

        print(f'end in time: {time.time() - start}')

        df.rename(columns={'PARCEL_ID': "apn", "PHY_ADDR1": "address_line_1", "PHY_ADDR2": "address_line_2"},
                  inplace=True)
        df.to_csv(output_path)
        print('Saved result table to .csv')

        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn, conn.begin():
            print("Creating table...")
            table_name = f'tmp_{self.county}_address'
            df.to_sql(table_name, conn, "public", if_exists="replace")
            print(f"Created temporary tmp_{self.county}_address_table table")

        db.session.execute(
            '''
            update property
            set
                address_line_1 = {}.address_line_1,
                address_line_2 = {}.address_line_2
            from {}
            where property.apn = {}.apn
            and county='{}'
            '''.format(table_name, table_name, table_name, table_name, self.county)
        )
        print(f'Updated address lines for the {self.county}')
        db.session.execute('DROP TABLE {}'.format(table_name))
        print("Removed temporary '{}' table".format(table_name))
        db.session.commit()
