from collections import OrderedDict

RULE_OBSOLESCENCE = 'obsolescence_rules'

FLORIDA_LOCATION_OBSO_CODES = {'OCEAN': 119, 'OCEAN VIEW': 120}


def get_florida_obsolescence(county):
    return OrderedDict([
        # below codes represent property land_use
        ('MULTI_FAMILY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 0,
            'code': 3,
            'county': county,
            'rule_name': 'Multi family 10 or more',
        }),
        ('VACANT_COMMERCIAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 1,
            'code': 10,
            'county': county,
            'rule_name': 'Vacant Commercial',
        }),
        ('STORES_ONE_STORY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 2,
            'code': 11,
            'county': county,
            'rule_name': 'Stores',
        }),
        ('MIXED_USE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 3,
            'code': 12,
            'county': county,
            'rule_name': 'Mixed use',
        }),
        ('DEPARTMENT_STORES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 4,
            'code': 13,
            'county': county,
            'rule_name': 'Department stores',
        }),
        ('SUPERMARKETS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 5,
            'code': 14,
            'county': county,
            'rule_name': 'Supermarkets',
        }),
        ('REGIONAL_SHOPPING_CENTERS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 6,
            'code': 15,
            'county': county,
            'rule_name': 'Regional Shopping Centers',
        }),
        ('COMMUNITY_SHOPPING_CENTERS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 7,
            'code': 16,
            'county': county,
            'rule_name': 'Community Shopping Centers',
        }),
        ('OFFICE_ONE_STORY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 8,
            'code': 17,
            'county': county,
            'rule_name': 'Office buildings',
        }),
        ('OFFICE_MULTI_STORY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 9,
            'code': 18,
            'county': county,
            'rule_name': 'Office buildings',
        }),
        ('PROFESSIONAL_SERVICE_BUILDINGS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 10,
            'code': 19,
            'county': county,
            'rule_name': 'Prof. service buildings',
        }),
        ('AIRPORTS_TERMINALS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 11,
            'code': 20,
            'county': county,
            'rule_name': 'Airports',
        }),
        ('RESTAURANTS_CAFETERIAS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 12,
            'code': 21,
            'county': county,
            'rule_name': 'Restaurants or Cafeterias',
        }),
        ('DRIVE_IN_RESTAURANTS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 13,
            'code': 22,
            'county': county,
            'rule_name': 'Drive in Restaurants',
        }),
        ('FINANCIAL_INSTITUTIONS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 14,
            'code': 23,
            'county': county,
            'rule_name': 'Financial institutions',
        }),
        ('INSURANCE_COMPANY_OFFICE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 15,
            'code': 24,
            'county': county,
            'rule_name': 'Insurance Company Office',
        }),
        ('REPAIR_SERVICE_SHOPS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 16,
            'code': 25,
            'county': county,
            'rule_name': 'Repair service shops',
        }),
        ('SERVICE_STATIONS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 17,
            'code': 26,
            'county': county,
            'rule_name': 'Service Stations',
        }),
        ('AUTO_SALES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 18,
            'code': 27,
            'county': county,
            'rule_name': 'Auto sales, auto repair',
        }),
        ('PARKING_LOTS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 19,
            'code': 28,
            'county': county,
            'rule_name': 'Parking lots',
        }),
        ('WHOLESALE_OUTLETS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 20,
            'code': 29,
            'county': county,
            'rule_name': 'Wholesale outlets',
        }),
        ('FLORISTS_GREENHOUSES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 21,
            'code': 30,
            'county': county,
            'rule_name': 'Florists, greenhouses',
        }),
        ('DRIVE_IN_THEATERS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 22,
            'code': 31,
            'county': county,
            'rule_name': 'Drive-in theaters',
        }),
        ('ENCLOSED_THEATERS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 23,
            'code': 32,
            'county': county,
            'rule_name': 'Enclosed theaters',
        }),
        ('NIGHTCLUBS_BARS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 24,
            'code': 33,
            'county': county,
            'rule_name': 'Nightclubs, bars',
        }),
        ('BOWLING_ALLEYS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 25,
            'code': 34,
            'county': county,
            'rule_name': 'Bowling alleys, recreation',
        }),
        ('TOURIST_ATTRACTIONS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 26,
            'code': 35,
            'county': county,
            'rule_name': 'Tourist attractions',
        }),
        ('CAMPS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 27,
            'code': 36,
            'county': county,
            'rule_name': 'Camps',
        }),
        ('RACE_TRACKS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 28,
            'code': 37,
            'county': county,
            'rule_name': 'Race tracks',
        }),
        ('GOLF_COURSES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 29,
            'code': 38,
            'county': county,
            'rule_name': 'Golf courses',
        }),
        ('HOTELS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 30,
            'code': 39,
            'county': county,
            'rule_name': 'Hotels, motels',
        }),
        ('VACANT_INDUSTRIAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 31,
            'code': 40,
            'county': county,
            'rule_name': 'Vacant Industrial',
        }),
        ('LIGHT_MANUFACTURING', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 32,
            'code': 41,
            'county': county,
            'rule_name': 'Light manufacturing',
        }),
        ('INSTRUMENT_MANUFACTURING', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 33,
            'code': 42,
            'county': county,
            'rule_name': 'Heavy industrial',
        }),
        ('LUMBER_YARDS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 34,
            'code': 43,
            'county': county,
            'rule_name': 'Lumber yards, sawmills',
        }),
        ('PARKING_PLANTS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 35,
            'code': 44,
            'county': county,
            'rule_name': 'Packing plants',
        }),
        ('CANNERIES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 36,
            'code': 45,
            'county': county,
            'rule_name': 'Canneries',
        }),
        ('CANDY_CHIP_FACTORIES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 37,
            'code': 46,
            'county': county,
            'rule_name': 'Other food processing',
        }),
        ('MINERAL_PROCESSING', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 38,
            'code': 47,
            'county': county,
            'rule_name': 'Mineral processing',
        }),
        ('WAREHOUSING', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 39,
            'code': 48,
            'county': county,
            'rule_name': 'Warehousing',
        }),
        ('OPEN_STORAGE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 40,
            'code': 49,
            'county': county,
            'rule_name': 'Open storage',
        }),
        ('VACANT_INSTITUTIONAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 41,
            'code': 70,
            'county': county,
            'rule_name': 'Vacant Institutional',
        }),
        ('CHURCHES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 42,
            'code': 71,
            'county': county,
            'rule_name': 'Churches',
        }),
        ('PRIVATE_SCHOOLS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 43,
            'code': 72,
            'county': county,
            'rule_name': 'Private schools',
        }),
        ('PRIVATE_HOSPITALS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 44,
            'code': 73,
            'county': county,
            'rule_name': 'Privately owned hospitals',
        }),
        ('HOMES_FOR_THE_AGED', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 45,
            'code': 74,
            'county': county,
            'rule_name': 'Homes for the aged',
        }),
        ('ORPHANAGES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 46,
            'code': 75,
            'county': county,
            'rule_name': 'Orphanages',
        }),
        ('CEMETERIES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 47,
            'code': 76,
            'county': county,
            'rule_name': 'Mortuaries, cemeteries',
        }),
        ('CLUBS_LODGES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 48,
            'code': 77,
            'county': county,
            'rule_name': 'Clubs, lodges, union hall',
        }),
        ('SANITARIUMS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 49,
            'code': 78,
            'county': county,
            'rule_name': 'Sanitariums, homes',
        }),
        ('CULTURAL_ORGANIZATIONS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 50,
            'code': 79,
            'county': county,
            'rule_name': 'Cultural organizations',
        }),
        ('VACANT_GOVERNMENTAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 51,
            'code': 80,
            'county': county,
            'rule_name': 'Vacant Governmental',
        }),
        ('MILITARY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 52,
            'code': 81,
            'county': county,
            'rule_name': 'Military',
        }),
        ('FOREST_PARKS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 53,
            'code': 82,
            'county': county,
            'rule_name': 'Forest, parks, recreation',
        }),
        ('PUBLIC_SCHOOLS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 54,
            'code': 83,
            'county': county,
            'rule_name': 'Public county schools',
        }),
        ('NON_PRIVATE_COLLEGES', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 55,
            'code': 84,
            'county': county,
            'rule_name': 'Colleges (non-private)',
        }),
        ('NON_PRIVATE_HOSPITALS', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 56,
            'code': 85,
            'county': county,
            'rule_name': 'Hospitals (non-private)',
        }),
        ('NON_MUNICIPAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 57,
            'code': 86,
            'county': county,
            'rule_name': 'Counties',
        }),
        ('STATE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 58,
            'code': 87,
            'county': county,
            'rule_name': 'State',
        }),
        ('FEDERAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 59,
            'code': 88,
            'county': county,
            'rule_name': 'Federal',
        }),
        ('MUNICIPAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 60,
            'code': 89,
            'county': county,
            'rule_name': 'Municipal',
        }),
        ('SEWAGE_DISPOSAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 61,
            'code': 96,
            'county': county,
            'rule_name': 'Sewage disposal',
        }),
        # below codes represent location
        ('OCEAN', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 62,
            'code': 119,
            'county': county,
            'rule_name': 'OCEAN VIEW',
        }),
        ('OCEAN_VIEW', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 63,
            'code': 120,
            'county': county,
            'rule_name': 'OCEAN',
        }),

        # last rule used to return 0 in case location is not an ocean view
        ('NO_LOCATION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 64,
            'code': 0,
            'county': county,
            'rule_name': 'None',
        }),

        # road obsolescenses
        ('BRIDLEWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 65,
            'code': 1000,
            'county': county,
            'rule_name': 'Bridleway',
        }),
        ('CONSTRUCTION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 66,
            'code': 1001,
            'county': county,
            'rule_name': 'Construction',
        }),
        ('MOTORWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 67,
            'code': 1002,
            'county': county,
            'rule_name': 'Motorway',
        }),
        ('MOTORWAY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 68,
            'code': 1003,
            'county': county,
            'rule_name': 'Motorway Link',
        }),
        ('PRIMARY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 69,
            'code': 1004,
            'county': county,
            'rule_name': 'Primary',
        }),
        ('PRIMARY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 70,
            'code': 1005,
            'county': county,
            'rule_name': 'Primary Link',
        }),
        ('RACEWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 71,
            'code': 1006,
            'county': county,
            'rule_name': 'Raceway',
        }),
        ('SECONDAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 72,
            'code': 1007,
            'county': county,
            'rule_name': 'Secondary',
        }),
        ('SECONDAY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 73,
            'code': 1008,
            'county': county,
            'rule_name': 'Secondary Link',
        }),
        ('TERTIARY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 74,
            'code': 1009,
            'county': county,
            'rule_name': 'Tertiary',
        }),
        ('TERTIARY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 75,
            'code': 1010,
            'county': county,
            'rule_name': 'Tertiary Link',
        }),
        ('TRACK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 76,
            'code': 1011,
            'county': county,
            'rule_name': 'Track',
        }),
        ('TRUNK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 77,
            'code': 1012,
            'county': county,
            'rule_name': 'Trunk',
        }),
        ('TRUNK_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 78,
            'code': 1013,
            'county': county,
            'rule_name': 'Trunk Link',
        }),
        ('RAILWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 78,
            'code': 1013,
            'county': county,
            'rule_name': 'Railway',
        }),
    ])


OBSOLESCENCE_SIMPLIFY_MAPPER = {
    # This mapper is used to reduce number of obsolescence we got in property rules
    # Please refer to asana task
    # https://app.asana.com/0/1147405519499344/1199369947141702
    # for more details and related excel files. which are:
    # Nassau and Suffolk County Land Tag Codes.xls
    # Obsolescence chart.xls
    'nassau': {
        8010: 0,
        1120: 35,
        1170: 35,
        1200: 35,
        1400: 35,
        1700: 35,
        2800: 3,
        4001: 29,
        4002: 29,
        4110: 25,
        4111: 25,
        4112: 25,
        4116: 25,
        4117: 25,
        4121: 25,
        4131: 25,
        4141: 3,
        4151: 3,
        4181: 3,
        4200: 3,
        4207: 1,
        4211: 1,
        4221: 1,
        4231: 1,
        4241: 1,
        4251: 1,
        4261: 1,
        4300: 1,
        4307: 1,
        4311: 1,
        4312: 1,
        4321: 1,
        4322: 1,
        4323: 1,
        4324: 1,
        4331: 1,
        4341: 1,
        4350: 1,
        4360: 1,
        4371: 40,
        4380: 40,
        4390: 40,
        4400: 24,
        4411: 7,
        4420: 7,
        4421: 7,
        4441: 1,
        4451: 1,
        4461: 1,
        4471: 1,
        4490: 24,
        4500: 24,
        4502: 24,
        4507: 1,
        4511: 24,
        4521: 24,
        4522: 24,
        4531: 24,
        4540: 24,
        4550: 24,
        4600: 24,
        4607: 24,
        4611: 24,
        4621: 24,
        4631: 24,
        4641: 24,
        4642: 24,
        4651: 24,
        4652: 41,
        4653: 41,
        4654: 41,
        4711: 41,
        4717: 41,
        4721: 7,
        4731: 1,
        4737: 1,
        4738: 1,
        4751: 7,
        4800: 7,
        4801: 7,
        4811: 1,
        4821: 1,
        4822: 1,
        4832: 40,
        4841: 40,
        4851: 40,
        4861: 40,
        5100: 40,
        5107: 40,
        5108: 40,
        5121: 40,
        5140: 40,
        5151: 40,
        5221: 7,
        5300: 7,
        5321: 7,
        5341: 7,
        5400: 7,
        5411: 7,
        5421: 7,
        5431: 7,
        5441: 7,
        5450: 7,
        5461: 30,
        5520: 30,
        5531: 27,
        5541: 30,
        5551: 39,
        5560: 30,
        5570: 30,
        5600: 30,
        5601: 30,
        5700: 30,
        5701: 30,
        5702: 30,
        5703: 1,
        5704: 1,
        5705: 1,
        5810: 30,
        5830: 30,
        5900: 30,
        5910: 30,
        5920: 30,
        6001: 28,
        6002: 28,
        6008: 28,
        6009: 23,
        6100: 29,
        6110: 29,
        6111: 29,
        6121: 29,
        6122: 29,
        6130: 29,
        6140: 29,
        6150: 29,
        6200: 28,
        6201: 28,
        6208: 28,
        6300: 3,
        6321: 3,
        6330: 3,
        6410: 7,
        6411: 7,
        6420: 7,
        6510: 7,
        6515: 7,
        6520: 7,
        6521: 7,
        6522: 7,
        6523: 7,
        6524: 25,
        6525: 40,
        6526: 40,
        6527: 40,
        6528: 40,
        6529: 40,
        6530: 40,
        6531: 40,
        6535: 40,
        6536: 40,
        6537: 40,
        6538: 40,
        6539: 40,
        6620: 1,
        6621: 1,
        6700: 1,
        6800: 1,
        6810: 1,
        6820: 1,
        6910: 1,
        6940: 1,
        6950: 31,
        6951: 31,
        7100: 7,
        7101: 7,
        7102: 7,
        7103: 7,
        7107: 7,
        7108: 7,
        7120: 7,
        7210: 7,
        8200: 36,
        8220: 36,
        8360: 7,
        8411: 7,
        8530: 36,
        9100: 35,
        9201: 35,
        9320: 35,
        9400: 35,
        9600: 30,
        9610: 30,
        9620: 30,
        9631: 30,
        9632: 30,
        9633: 30,
        9700: 30,
        9710: 30,

        # roads mapper
        # this is a two step mapper
        # first from name we get code
        # secondly from code we get the index via get_index_from_code
        'trunk': '10001',
        '10001': 21,
        'secondary': '10001',
        'trunk_link': '10001',
        'tertiary': '10002',
        '10002': 22,
        'secondary_link': '10001',
        'tertiary_link': '10001',
        'bridleway': '10003',
        '10003': 8,
        'construction': '10004',
        '10004': 39,
        'raceway': '10001',
        'primary': '10001',
        'track': '10005',
        '10005': 23,
        'primary_link': '10001',
        'motorway_link': '10001',
        'railway': '10005',
        'motorway': '10002'

    },
}

ALL_OBSOLESCENCE = {
    'nassau': OrderedDict([
        ('NASSAU_NO_LOCATION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 0,
            'code': 0,
            'county': 'nassau',
            'rule_name': 'NO LOCATION',
        }),
        ('NASSAU_BUSINESS_DISTRICT', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 1,
            'code': 1,
            'county': 'nassau',
            'rule_name': 'CENTRAL BUSINESS DISTRICT',
        }),
        ('NASSAU_PERIM_CENTRAL_BUSINESS_DISTRICT', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 2,
            'code': 2,
            'county': 'nassau',
            'rule_name': 'PERIM CENTRAL BUSINESS DISTRICT',
        }),
        ('NASSAU_BUSINESS_CLUSTER', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 3,
            'code': 3,
            'county': 'nassau',
            'rule_name': 'BUSINESS CLUSTER',
        }),
        ('NASSAU_MAJOR_STRIP', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 4,
            'code': 4,
            'county': 'nassau',
            'rule_name': 'MAJOR STRIP',
        }),
        ('NASSAU_SECONDARY_STRIP', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 5,
            'code': 5,
            'county': 'nassau',
            'rule_name': 'SECONDARY STRIP',
        }),
        ('NASSAU_NEIGHBORHOOD_OR_SPOT', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 6,
            'code': 6,
            'county': 'nassau',
            'rule_name': 'NEIGHBORHOOD OR SPOT',
        }),
        ('NASSAU_COMMERCIAL_INDUSTRIAL_PARK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 7,
            'code': 7,
            'county': 'nassau',
            'rule_name': 'COMMERCIAL/INDUSTRIAL PARK',
        }),
        ('NASSAU_APARTMENT_CONDO_COMPLEX', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 8,
            'code': 8,
            'county': 'nassau',
            'rule_name': 'APARTMENT/CONDO COMPLEX',
        }),
        ('NASSAU_NO_LOCATIONAL_INFLUENCE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 9,
            'code': 20,
            'county': 'nassau',
            'rule_name': 'NO LOCATIONAL INFLUENCE',
        }),
        ('NASSAU_MAJOR_HIGHWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 10,
            'code': 21,
            'county': 'nassau',
            'rule_name': 'MAJOR HIGHWAY',
        }),
        ('NASSAU_SECONDARY_STREET', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 11,
            'code': 22,
            'county': 'nassau',
            'rule_name': 'SECONDARY STREET',
        }),
        ('NASSAU_LONG_ISLAND_RAIL_ROAD', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 12,
            'code': 23,
            'county': 'nassau',
            'rule_name': 'LONG ISLAND RAIL ROAD',
        }),
        ('NASSAU_COMMERCIAL_OR_INDUSTRIAL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 13,
            'code': 24,
            'county': 'nassau',
            'rule_name': 'COMMERCIAL OR INDUSTRIAL',
        }),
        ('NASSAU_APARTMENT_BUILDING', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 14,
            'code': 25,
            'county': 'nassau',
            'rule_name': 'APARTMENT BUILDING',
        }),
        ('NASSAU_CONTAMINATED_SITE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 15,
            'code': 26,
            'county': 'nassau',
            'rule_name': 'CONTAMINATED SITE',
        }),
        ('NASSAU_GOLD_COURSE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 16,
            'code': 27,
            'county': 'nassau',
            'rule_name': 'GOLF COURSE',
        }),
        ('NASSAU_RELIGIOUS_INSTITUTION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 17,
            'code': 28,
            'county': 'nassau',
            'rule_name': 'RELIGIOUS INSTITUTION',
        }),
        ('NASSAU_SCHOOL', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 18,
            'code': 29,
            'county': 'nassau',
            'rule_name': 'SCHOOL',
        }),
        ('NASSAU_PARK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 19,
            'code': 30,
            'county': 'nassau',
            'rule_name': 'PARK',
        }),
        ('NASSAU_CEMETERY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 20,
            'code': 31,
            'county': 'nassau',
            'rule_name': 'CEMETERY',
        }),
        ('NASSAU_ABUTS_FIRE_STATION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 21,
            'code': 32,
            'county': 'nassau',
            'rule_name': 'ABUTS FIRE STATION',
        }),
        ('NASSAU_SPLIT_SCHOOL_DISTRICT', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 22,
            'code': 33,
            'county': 'nassau',
            'rule_name': 'SPLIT SCHOOL DISTRICT',
        }),
        ('NASSAU_NOISE', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 23,
            'code': 34,
            'county': 'nassau',
            'rule_name': 'NOISE',
        }),
        ('NASSAU_SUMP', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 24,
            'code': 35,
            'county': 'nassau',
            'rule_name': 'SUMP',
        }),
        ('NASSAU_WATER_SUPPLY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 25,
            'code': 36,
            'county': 'nassau',
            'rule_name': 'WATER SUPPLY',
        }),
        ('NASSAU_BACKS_PARKING_LOT', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 26,
            'code': 37,
            'county': 'nassau',
            'rule_name': 'BACKS PARKING LOT',
        }),
        ('NASSAU_SCHOOL_BALL_FIELD', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 27,
            'code': 38,
            'county': 'nassau',
            'rule_name': 'SCHOOL BALL FIELD',
        }),
        ('NASSAU_EXTERNAL_PERCENT_3', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 28,
            'code': 39,
            'county': 'nassau',
            'rule_name': 'LOCATION ADJ 3%',
        }),
        ('NASSAU_EXTERNAL_PERCENT_5', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 29,
            'code': 40,
            'county': 'nassau',
            'rule_name': 'LOCATION ADJ 5%',
        }),
        ('NASSAU_EXTERNAL_PERCENT_7', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 30,
            'code': 41,
            'county': 'nassau',
            'rule_name': 'LOCATION ADJ 7%',
        }),
        ('NASSAU_EXTERNAL_PERCENT_10', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 31,
            'code': 42,
            'county': 'nassau',
            'rule_name': 'LOCATION ADJ 10%',
        }),
        ('NASSAU_NO_WATER_1', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 32,
            'code': 43,
            'county': 'nassau',
            'rule_name': 'NO WATER 1',
        }),
        ('NASSAU_NO_WATER_2', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 33,
            'code': 44,
            'county': 'nassau',
            'rule_name': 'NO WATER 2',
        }),

        # ('NO_LOCATION', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': None,
        #     'code': 0,
        #     'county': 'nassau',
        #     'rule_name': 'None',
        # }),
        #
        # ('DAIRY_PRODUCT_MILK_BUTTER_CHEESE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 0,
        #     'code': 1120,
        #     'county': 'nassau',
        #     'rule_name': '4-Dairy Product, Milk, Butter, Cheese',
        # }),
        #
        # ('HORSE_FARMS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 1,
        #     'code': 1170,
        #     'county': 'nassau',
        #     'rule_name': '4-Horse Farms',
        # }),
        #
        # ('FIELD_CROPS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 2,
        #     'code': 1200,
        #     'county': 'nassau',
        #     'rule_name': '4-Field Crops',
        # }),
        #
        # ('TRUCK_CROPS_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 3,
        #     'code': 1400,
        #     'county': 'nassau',
        #     'rule_name': '4-Truck Crops Other',
        # }),
        #
        # ('NURSERIES_AND_GREENHOUSES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 4,
        #     'code': 1700,
        #     'county': 'nassau',
        #     'rule_name': '4-Nurseries and Greenhouses',
        # }),
        #
        # ('MULTIPLE_RESIDENCES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 5,
        #     'code': 2800,
        #     'county': 'nassau',
        #     'rule_name': '1-Multiple Residences',
        # }),
        #
        # ('RESIDENTIAL_LAND_WITH_SMALL_IMPORVEMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 6,
        #     'code': 3121,
        #     'county': 'nassau',
        #     'rule_name': '1-Residential Land w/ Small Improvement',
        # }),
        #
        # ('LOTS_OF_10_ACRES_OR_LESS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 7,
        #     'code': 3140,
        #     'county': 'nassau',
        #     'rule_name': '4-Lots of 10 Acres or Less',
        # }),
        #
        # ('UNDERWATER_LAND', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 8,
        #     'code': 3150,
        #     'county': 'nassau',
        #     'rule_name': '4-Underwater Land',
        # }),
        #
        # ('WATER_FRONT_LAND_WITH_SMALL_IMPROVEMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 9,
        #     'code': 3160,
        #     'county': 'nassau',
        #     'rule_name': '1-Water Front Land w/ Small Improvement',
        # }),
        #
        # ('CHILD_CARE_CENTER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 10,
        #     'code': 4001,
        #     'county': 'nassau',
        #     'rule_name': '4-Child Care Center',
        # }),
        #
        # ('PRIVATE_SCHOOL_FOR_PROFIT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 11,
        #     'code': 4002,
        #     'county': 'nassau',
        #     'rule_name': '4-Private School for Profit',
        # }),
        #
        # ('PAVING_OR_FENCING_WITH_HOTELS_OR_MOTELS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 12,
        #     'code': 4108,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving or Fencing with Hotels/Motels',
        # }),
        #
        # ('APARTMENTS_OTHER_THAN_CONDO_AND_CO_OPS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 13,
        #     'code': 4110,
        #     'county': 'nassau',
        #     'rule_name': '2-Apartments other than Condo & Co-ops',
        # }),
        #
        # ('OVER_6_FAMILY_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 14,
        #     'code': 4111,
        #     'county': 'nassau',
        #     'rule_name': '2-Over 6 Family Apartments',
        # }),
        #
        # ('4_TO_6_FAMILY_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 15,
        #     'code': 4112,
        #     'county': 'nassau',
        #     'rule_name': '2-4 - 6 Family Apartments',
        # }),
        #
        # ('ELEVATOR_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 16,
        #     'code': 4116,
        #     'county': 'nassau',
        #     'rule_name': '2-Elevator Apartments',
        # }),
        #
        # ('SMALL_IMPROVE_USED_WITH_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 17,
        #     'code': 4117,
        #     'county': 'nassau',
        #     'rule_name': '2-Small Improve used with Apartments',
        # }),
        #
        # ('PAVING_OR_FENCING_USED_WITH_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 18,
        #     'code': 4118,
        #     'county': 'nassau',
        #     'rule_name': '2-Paving or Fencing used with Apartments',
        # }),
        #
        # ('CONDOMINIUMS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 19,
        #     'code': 4121,
        #     'county': 'nassau',
        #     'rule_name': '2-Condominiums',
        # }),
        #
        # ('RES_PARKING_SPACES_OR_COMMON_ELEMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 20,
        #     'code': 4127,
        #     'county': 'nassau',
        #     'rule_name': '2-Res parking spaces/common Elements',
        # }),
        #
        # ('CO_OPERATIVE_APARTMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 21,
        #     'code': 4131,
        #     'county': 'nassau',
        #     'rule_name': '2-Co-Operative Apartments',
        # }),
        #
        # ('SMALL_IMPROVEMENTS_WITH_CO_OP', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 22,
        #     'code': 4137,
        #     'county': 'nassau',
        #     'rule_name': '2-Small Improvements with Co-Op',
        # }),
        #
        # ('PAVING_OR_FENCING_USED_WITH_CO_OP', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 23,
        #     'code': 4138,
        #     'county': 'nassau',
        #     'rule_name': '2-Paving or Fencing used with Co-Op',
        # }),
        #
        # ('HOTELS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 24,
        #     'code': 4141,
        #     'county': 'nassau',
        #     'rule_name': '4-Hotels',
        # }),
        #
        # ('MOTELS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 25,
        #     'code': 4151,
        #     'county': 'nassau',
        #     'rule_name': '4-Motels',
        # }),
        #
        # ('INNS_LODGES_BOARDING_OR_ROOMING_HOUSES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 26,
        #     'code': 4181,
        #     'county': 'nassau',
        #     'rule_name': '4-Inns, Lodges, Boarding/Rooming Houses',
        # }),
        #
        # ('DINING_ESTABLISHMENTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 27,
        #     'code': 4200,
        #     'county': 'nassau',
        #     'rule_name': '4-Dining Establishments',
        # }),
        #
        # ('SMALL_IMPROVE_USED_WITH_RESTAURANTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 28,
        #     'code': 4207,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improve used with Restaurants',
        # }),
        #
        # ('PAVING_OR_FENCING_USED_WITH_REST', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 29,
        #     'code': 4208,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving or Fencing used with Rest.',
        # }),
        #
        # ('RESTAURANTS_FULL_SERVICE_AND_BEVARAGE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 30,
        #     'code': 4211,
        #     'county': 'nassau',
        #     'rule_name': '4-Restaurants, Full Service and Beverage',
        # }),
        #
        # ('DINERS_COUNTER_SERVICE_LIMITED_MENU', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 31,
        #     'code': 4221,
        #     'county': 'nassau',
        #     'rule_name': '4-Diners, Counter Service, Limited Menu',
        # }),
        #
        # ('ROAD_STANDS_SMALL_STORES_DAIRY_BARNS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 32,
        #     'code': 4231,
        #     'county': 'nassau',
        #     'rule_name': '4-Road Stands, Small Stores, Dairy Barns',
        # }),
        #
        # ('NIGHT_CLUB_AND_DINER_THEATERS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 33,
        #     'code': 4241,
        #     'county': 'nassau',
        #     'rule_name': '4-Night Club and Dinner Theaters',
        # }),
        #
        # ('BARS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 34,
        #     'code': 4251,
        #     'county': 'nassau',
        #     'rule_name': '4-Bars',
        # }),
        #
        # ('FAST_FOOD_FACILITY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 35,
        #     'code': 4261,
        #     'county': 'nassau',
        #     'rule_name': '4-Fast Food Facility',
        # }),
        #
        # ('MOTOR_VEHICLE_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 36,
        #     'code': 4300,
        #     'county': 'nassau',
        #     'rule_name': '4-Motor Vehicle Services',
        # }),
        #
        # ('SMALL_IMPROVE_USED_WITH_MOTER_VEHICLES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 37,
        #     'code': 4307,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improve Used with Motor Vehicles',
        # }),
        #
        # ('PAVING_OR_FENCING_USED_WITH_MOTOR_VEHICLE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 38,
        #     'code': 4308,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving or Fencing used with Motor Veh',
        # }),
        #
        # ('AUTO_DEALERS_SALES_AND_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 39,
        #     'code': 4311,
        #     'county': 'nassau',
        #     'rule_name': '4-Auto Dealers, Sales and Service',
        # }),
        #
        # ('AUTO_SALES_USED_CAR_LOT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 40,
        #     'code': 4312,
        #     'county': 'nassau',
        #     'rule_name': '4-Auto Sales, Used Car Lot',
        # }),
        #
        # ('GAS_STATIONS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 41,
        #     'code': 4321,
        #     'county': 'nassau',
        #     'rule_name': '4- Gas Stations',
        # }),
        #
        # ('GAS_AND_CONVENIENCE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 42,
        #     'code': 4322,
        #     'county': 'nassau',
        #     'rule_name': '4-Gas and Convenience',
        # }),
        #
        # ('GAS_AND_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 43,
        #     'code': 4323,
        #     'county': 'nassau',
        #     'rule_name': '4- Gas and Service',
        # }),
        #
        # ('GAS_CONVINIENCE_AND_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 44,
        #     'code': 4324,
        #     'county': 'nassau',
        #     'rule_name': '4- Gas, Convenience and  Service',
        # }),
        #
        # ('COMMERCIAL_GARAGE_REPAIRS_TIRE_SHOPS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 45,
        #     'code': 4331,
        #     'county': 'nassau',
        #     'rule_name': '4-Commercial Garage Repairs, Tire Shops',
        # }),
        #
        # ('AUTOMATIC_CAR_WASH', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 46,
        #     'code': 4341,
        #     'county': 'nassau',
        #     'rule_name': '4-Automatic Car Wash',
        # }),
        #
        # ('MANUAL_CAR_WASH', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 47,
        #     'code': 4350,
        #     'county': 'nassau',
        #     'rule_name': '4-Manual Car Wash',
        # }),
        #
        # ('SELF_SERVICE_CAR_WASH_COIN_OPERATED', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 48,
        #     'code': 4360,
        #     'county': 'nassau',
        #     'rule_name': '4-Self Service Car Wash - Coin Operated',
        # }),
        #
        # ('PARKING_GARAGE_MULTI_STORY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 49,
        #     'code': 4370,
        #     'county': 'nassau',
        #     'rule_name': '4-Parking Garage - Multi Story',
        # }),
        #
        # ('PARKING_LOT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 50,
        #     'code': 4380,
        #     'county': 'nassau',
        #     'rule_name': '4-Parking Lot',
        # }),
        #
        # ('SMALL_GARAGE_FOR_PARKING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 51,
        #     'code': 4390,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Garage for Parking',
        # }),
        #
        # ('STORAGE_WAREHOUSE_AND_DIST_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 52,
        #     'code': 4400,
        #     'county': 'nassau',
        #     'rule_name': '4-Storage, Warehouse and Dist Facilities',
        # }),
        #
        # ('PAVING_OR_FENCING_WITH_STORAGE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 53,
        #     'code': 4408,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving or Fencing with Storage bldg',
        # }),
        #
        # ('FUEL_STORAGE_GASOLINE_FUEL_OIL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 54,
        #     'code': 4411,
        #     'county': 'nassau',
        #     'rule_name': '4-Fuel Storage - Gasoline, Fuel, Oil',
        # }),
        #
        # ('BOTTLED_GAS_NATURAL_GAS_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 55,
        #     'code': 4420,
        #     'county': 'nassau',
        #     'rule_name': '4-Bottled Gas, Natural Gas Facilities',
        # }),
        #
        # ('SELF_STORAGE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 55,
        #     'code': 4421,
        #     'county': 'nassau',
        #     'rule_name': '4-Self Storage',
        # }),
        #
        # ('LUMBER_YARDS_SALES_AND_STORAGE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 56,
        #     'code': 4441,
        #     'county': 'nassau',
        #     'rule_name': '4-Lumber Yards (Sales and Storage)',
        # }),
        #
        # ('COAL_YARDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 57,
        #     'code': 4451,
        #     'county': 'nassau',
        #     'rule_name': '4-Coal Yards',
        # }),
        #
        # ('COLD_STORAGE_OR_FROZEN_FOOD_PLANTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 57,
        #     'code': 4461,
        #     'county': 'nassau',
        #     'rule_name': '4-Cold Storage or Frozen food Plants',
        # }),
        #
        # ('TRUCK_TERMINALS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 57,
        #     'code': 4471,
        #     'county': 'nassau',
        #     'rule_name': '4-Truck Terminals',
        # }),
        #
        # ('PIERS_WHARVES_DOCKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 57,
        #     'code': 4480,
        #     'county': 'nassau',
        #     'rule_name': '4-Piers, Wharves, Docks',
        # }),
        #
        # ('STORAGE_WAREHOUSE_AND_DIST_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 58,
        #     'code': 4490,
        #     'county': 'nassau',
        #     'rule_name': '4-Storage, Warehouse and Dist Facilities',
        # }),
        #
        # ('RETAIL_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 59,
        #     'code': 4500,
        #     'county': 'nassau',
        #     'rule_name': '4-Retail Service',
        # }),
        #
        # ('RETAIL_CONDOMINIUM', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 60,
        #     'code': 4502,
        #     'county': 'nassau',
        #     'rule_name': '4-Retail Condominium',
        # }),
        #
        # ('SMALL_IMPROVEMENT_FOR_RETAIL_SERVICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 61,
        #     'code': 4507,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improvement for Retail Service',
        # }),
        #
        # ('PAVING_FENCING_USED_FOR_RETAIL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 62,
        #     'code': 4508,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving Fencing used for Retail',
        # }),
        #
        # ('REGIONAL_SHOPPING_CENTER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 63,
        #     'code': 4511,
        #     'county': 'nassau',
        #     'rule_name': '4-Regional Shopping Center',
        # }),
        #
        # ('AREA_NEIGHBORHOOD_SHOPPING_CENTER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 64,
        #     'code': 4521,
        #     'county': 'nassau',
        #     'rule_name': '4-Area/Neighborhood Shopping Center',
        # }),
        #
        # ('CONDO_STRIP_STORES_RETAIL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 65,
        #     'code': 4522,
        #     'county': 'nassau',
        #     'rule_name': '4-Condo Strip Stores - Retail',
        # }),
        #
        # ('DEPARTMENT_STORE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 66,
        #     'code': 4531,
        #     'county': 'nassau',
        #     'rule_name': '4-Department Store',
        # }),
        #
        # ('DISCOUNT_HOUSED', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 67,
        #     'code': 4532,
        #     'county': 'nassau',
        #     'rule_name': '4-Discount Housed',
        # }),
        #
        # ('LARGE_RETAIL_FOOD_STORE_SUPERMARKET', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 68,
        #     'code': 4540,
        #     'county': 'nassau',
        #     'rule_name': '4-Large Retail Food Store - Supermarket',
        # }),
        #
        # ('DEALERSHIPS_SALES_SERVICE_NON_AUTO', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 69,
        #     'code': 4550,
        #     'county': 'nassau',
        #     'rule_name': '4-Dealerships Sales/Service (non-Auto)',
        # }),
        #
        # ('BANKS_AND_OFFICE_BUILDINGS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 70,
        #     'code': 4600,
        #     'county': 'nassau',
        #     'rule_name': '4-Banks and Office Buildings',
        # }),
        #
        # ('SMALL_IMPROVEMENT_USED_WITH_BANKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 71,
        #     'code': 4607,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improvement used with Banks',
        # }),
        #
        # ('PAVING_FENCING_USED_WITH_BANKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 72,
        #     'code': 4608,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving, Fencing used with Banks',
        # }),
        #
        # ('STANDARD_BANK_SINGLE_OCCUPANCY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 73,
        #     'code': 4611,
        #     'county': 'nassau',
        #     'rule_name': '4-Standard Bank (Single Occupancy)',
        # }),
        #
        # ('DRIVE_IN_BANK_ISLAND_TYPE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 74,
        #     'code': 4621,
        #     'county': 'nassau',
        #     'rule_name': '4-Drive in Bank (Island type)',
        # }),
        #
        # ('BANK_BUILDING_WITH_OFFICES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 75,
        #     'code': 4631,
        #     'county': 'nassau',
        #     'rule_name': '4-Bank Building with Offices',
        # }),
        #
        # ('OFFICE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 76,
        #     'code': 4641,
        #     'county': 'nassau',
        #     'rule_name': '4-Office Building',
        # }),
        #
        # ('CONDOMINIUM_OFFICE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 77,
        #     'code': 4642,
        #     'county': 'nassau',
        #     'rule_name': '4-Condominium Office Building',
        # }),
        #
        # ('PROFESSIONAL_OFFICE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 78,
        #     'code': 4651,
        #     'county': 'nassau',
        #     'rule_name': '4-Professional Office Building',
        # }),
        #
        # ('HOSPITAL_NON_EXEMPT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 79,
        #     'code': 4652,
        #     'county': 'nassau',
        #     'rule_name': '4-Hospital - Non Exempt',
        # }),
        #
        # ('NURSING_HOMES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 80,
        #     'code': 4653,
        #     'county': 'nassau',
        #     'rule_name': '4-Nursing Homes',
        # }),
        #
        # ('ASSISTED_LIVING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 81,
        #     'code': 4654,
        #     'county': 'nassau',
        #     'rule_name': 'Assisted Living',
        # }),
        #
        # ('FUNEAL_HOMES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 82,
        #     'code': 4711,
        #     'county': 'nassau',
        #     'rule_name': '4-Funeral Homes',
        # }),
        #
        # ('SMALL_IMPROVEMENT_USED_WITH_FUNERAL_HOMES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 83,
        #     'code': 4717,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improvement used w/Funeral Homes',
        # }),
        #
        # ('PAVING_BLACKTOP_FENC_WITH_FUNERAL_HOMES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 84,
        #     'code': 4718,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving, blacktop, fenc w/Funeral Homes',
        # }),
        #
        # ('VETERINARY_CLINICSAND_KENNELS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 85,
        #     'code': 4721,
        #     'county': 'nassau',
        #     'rule_name': '4-Veterinary Clinicsand Kennels',
        # }),
        #
        # ('PAVING_FENCES_USED_WITH_VET_CLINICS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 86,
        #     'code': 4728,
        #     'county': 'nassau',
        #     'rule_name': '4 - Paving, fences  used w/Vet clinics',
        # }),
        #
        # ('GREENHOUSES_NURSERIES_GARDEN_CTR', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 87,
        #     'code': 4731,
        #     'county': 'nassau',
        #     'rule_name': '4 - Greenhouses, Nurseries & Garden Ctr',
        # }),
        #
        # ('SMALL_IMPROV_USED_WITH_GARDEN_CTR', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 88,
        #     'code': 4737,
        #     'county': 'nassau',
        #     'rule_name': '4 - Small Improv used w/ Garden Ctr',
        # }),
        #
        # ('PAVING_FENCES_USED_WITH_GARDEN_CTR', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 89,
        #     'code': 4738,
        #     'county': 'nassau',
        #     'rule_name': '4 - Paving, fences used w/ Garden Ctr',
        # }),
        #
        # ('JUNKYARDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 90,
        #     'code': 4751,
        #     'county': 'nassau',
        #     'rule_name': '4 - Junkyards',
        # }),
        #
        # ('MULTI_USE_OR_MULTI_PURPOSE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 91,
        #     'code': 4800,
        #     'county': 'nassau',
        #     'rule_name': '4 - Multi Use or Multi Purpose Bldg',
        # }),
        #
        # ('MULTI_USE_BUILDINB_WITH_ATT_DWELLING_OR_APT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 92,
        #     'code': 4801,
        #     'county': 'nassau',
        #     'rule_name': '4 - Multi Use Bldg w/Att Dwelling or Apt',
        # }),
        #
        # ('PAVING_FENCE_MULTI_USE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 93,
        #     'code': 4807,
        #     'county': 'nassau',
        #     'rule_name': '4 - Paving, Fence Muli Use Bldg',
        # }),
        #
        # ('PAVING_OR_FENCING_WITH_MULTI_USE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 94,
        #     'code': 4808,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving or fencing with Multi Use Bldg',
        # }),
        #
        # ('ROW_TYPE_STORE_WITH_COMMON_WALLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 95,
        #     'code': 4811,
        #     'county': 'nassau',
        #     'rule_name': '4-Row Type Store w/ Common  Walls',
        # }),
        #
        # ('ROW_TYPE_STORE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 96,
        #     'code': 4821,
        #     'county': 'nassau',
        #     'rule_name': '4-Row Type Store',
        # }),
        #
        # ('ROW_TYPE_STORE_DET_NO_PARTY_WALLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 97,
        #     'code': 4822,
        #     'county': 'nassau',
        #     'rule_name': '4-Row Type Store Det, no Party Walls',
        # }),
        #
        # ('CONVERTED_RESIDENCE_PRIMARY_USE_RES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 98,
        #     'code': 4830,
        #     'county': 'nassau',
        #     'rule_name': '1-Converted Residence - primary use Res',
        # }),
        #
        # ('CONVERTED_RES_PRIMARY_USE_NON_RES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 99,
        #     'code': 4831,
        #     'county': 'nassau',
        #     'rule_name': '4-Converted Res - primary use Non-Res',
        # }),
        #
        # ('CONVERTED_RES_ROOMING_HOUSE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 100,
        #     'code': 4832,
        #     'county': 'nassau',
        #     'rule_name': '4-Converted Res - rooming house',
        # }),
        #
        # ('STORY_MULTI_USE_BUILDING_SINGLE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 101,
        #     'code': 4841,
        #     'county': 'nassau',
        #     'rule_name': '4-1 Story Multi-Use Building - Single',
        # }),
        #
        # ('STORY_MULTI_USE_BUILDING_MULTI', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 102,
        #     'code': 4851,
        #     'county': 'nassau',
        #     'rule_name': '4-1 Story Multi-Use Building - Multi',
        # }),
        #
        # ('MINI_MART', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 103,
        #     'code': 4861,
        #     'county': 'nassau',
        #     'rule_name': '4-Mini Mart',
        # }),
        #
        # ('ENTERTAINMENT_ASSEMBLY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 104,
        #     'code': 5100,
        #     'county': 'nassau',
        #     'rule_name': '4-Entertainment Assembly',
        # }),
        #
        # ('SMALL_IMPROVE_FOR_REC_AND_ENTERTAINMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 105,
        #     'code': 5107,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improve for Rec & Entertainment',
        # }),
        #
        # ('PAVING_FOR_RECREATION_AND_ENTERTAINMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 106,
        #     'code': 5108,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving for Recreation & Entertainment',
        # }),
        #
        # ('MOTION_PICTURE_THEATER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 107,
        #     'code': 5121,
        #     'county': 'nassau',
        #     'rule_name': '4-Motion Picture Theater',
        # }),
        #
        # ('AUDITORIUMS_EXHIBITIONS_AND_EXPO_HALLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 108,
        #     'code': 5140,
        #     'county': 'nassau',
        #     'rule_name': '4-Auditoriums, Exhibition and Expo Halls',
        # }),
        #
        # ('RADIO_TV_STATIONS_AND_MOTION_STUDIOS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 109,
        #     'code': 5151,
        #     'county': 'nassau',
        #     'rule_name': '4-Radio, TV Stations and Motion Studios',
        # }),
        #
        # ('RACETRACKS_AUTO_AND_HORSE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 110,
        #     'code': 5221,
        #     'county': 'nassau',
        #     'rule_name': '4-Racetracks: Auto and Horse',
        # }),
        #
        # ('AMUSEMENT_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 111,
        #     'code': 5300,
        #     'county': 'nassau',
        #     'rule_name': '4-Amusement Facilities',
        # }),
        #
        # ('AMUSEMENT_PARKS_OR_RIDES_KIDDLE_PARKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 112,
        #     'code': 5321,
        #     'county': 'nassau',
        #     'rule_name': '4-Amusement Parks or Rides, Kiddie Parks',
        # }),
        #
        # ('SOCIAL_ORGANIZATIONS_LODGE_HALLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 113,
        #     'code': 5341,
        #     'county': 'nassau',
        #     'rule_name': '4-Social Organizations, Lodge Halls',
        # }),
        #
        # ('INDOOR_SPORTS_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 114,
        #     'code': 5400,
        #     'county': 'nassau',
        #     'rule_name': '4-Indoor Sports Facilities',
        # }),
        #
        # ('BOWLING_ALLEYS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 115,
        #     'code': 5411,
        #     'county': 'nassau',
        #     'rule_name': '4-Bowling Alleys',
        # }),
        #
        # ('INDOOR_SKATING_RINKS_ROLLER_OR_ICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 116,
        #     'code': 5421,
        #     'county': 'nassau',
        #     'rule_name': '4-Indoor Skating Rinks, roller or Ice',
        # }),
        #
        # ('YMCA_YMHA', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 117,
        #     'code': 5431,
        #     'county': 'nassau',
        #     'rule_name': '4-YMCA, YMHA',
        # }),
        #
        # ('HEALTH_SPA', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 118,
        #     'code': 5441,
        #     'county': 'nassau',
        #     'rule_name': '4-Health Spa',
        # }),
        #
        # ('INDOOR_SWIMMING_POOLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 119,
        #     'code': 5450,
        #     'county': 'nassau',
        #     'rule_name': '4-Indoor Swimming Pools',
        # }),
        #
        # ('INDOOR_TENNIS_CLUBS_ARCHERY_BILLIARD', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 120,
        #     'code': 5461,
        #     'county': 'nassau',
        #     'rule_name': '4-Indoor Tennis Clubs, Archery, Billiard',
        # }),
        #
        # ('PUBLIC_GOLF_COURSES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 121,
        #     'code': 5520,
        #     'county': 'nassau',
        #     'rule_name': '4-Public Golf Courses',
        # }),
        #
        # ('COUNTRY_CLUBS_MEMBERSHIP_GOLF_COURSES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 122,
        #     'code': 5531,
        #     'county': 'nassau',
        #     'rule_name': '4-Country Clubs, Membership golf Courses',
        # }),
        #
        # ('COMMERICAL_OUTDOOR_SWIMMING_POOLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 123,
        #     'code': 5541,
        #     'county': 'nassau',
        #     'rule_name': '4-Commercial Outdoor Swimming Pools',
        # }),
        #
        # ('RIDING_STABLES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 124,
        #     'code': 5551,
        #     'county': 'nassau',
        #     'rule_name': '4-Riding Stables',
        # }),
        #
        # ('OUTDOOR_SKATING_ICE_OR_ROLLER_RINKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 125,
        #     'code': 5560,
        #     'county': 'nassau',
        #     'rule_name': '4-Outdoor Skating: Ice or Roller Rinks',
        # }),
        #
        # ('OUTDOOR_TENNIS_MINI_GOLF_BB_CAGES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 126,
        #     'code': 5570,
        #     'county': 'nassau',
        #     'rule_name': '4-Outdoor Tennis, Mini Golf, BB Cages',
        # }),
        #
        # ('BEACH_CLUB_MEMBERSHIP_CLUBS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 127,
        #     'code': 5600,
        #     'county': 'nassau',
        #     'rule_name': '4-Beach Club - Membership Clubs',
        # }),
        #
        # ('BEACH_CLUB_PRIVATE_NON_EXEMPT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 128,
        #     'code': 5601,
        #     'county': 'nassau',
        #     'rule_name': '4-Beach Club - Private - Non-Exempt',
        # }),
        #
        # ('MARINE_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 129,
        #     'code': 5700,
        #     'county': 'nassau',
        #     'rule_name': '4-Marine Facilities',
        # }),
        #
        # ('MARINES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 130,
        #     'code': 5701,
        #     'county': 'nassau',
        #     'rule_name': '4-Marinas',
        # }),
        #
        # ('YACHT_CLUB_PRIVATE_MEMBERSHIP_CLUB', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 131,
        #     'code': 5702,
        #     'county': 'nassau',
        #     'rule_name': '4-Yacht Club, Private membership Club',
        # }),
        #
        # ('BOAT_SALES_OR_REPAIRS_AND_STORAGE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 132,
        #     'code': 5703,
        #     'county': 'nassau',
        #     'rule_name': '4-Boat Sales or Repairs and Storage',
        # }),
        #
        # ('BOAT_REPAIRS_DOCKS_SLIPS_NO_BOAT_SALES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 133,
        #     'code': 5704,
        #     'county': 'nassau',
        #     'rule_name': '4-Boat Repairs,Docks,Slips-No Boat Sales',
        # }),
        #
        # ('SMALL_MARINE_FACILITIES_BAIT_FUELING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 134,
        #     'code': 5705,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Marine Facilities, Bait,Fueling',
        # }),
        #
        # ('CAMPS_SLEEPAWAY_FOR_GROUPS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 135,
        #     'code': 5810,
        #     'county': 'nassau',
        #     'rule_name': '4-Camps: Sleepaway for Groups',
        # }),
        #
        # ('RESORT_COMPLEXES_RESORT_HOTELS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 136,
        #     'code': 5830,
        #     'county': 'nassau',
        #     'rule_name': '4-Resort Complexes, Resort Hotels',
        # }),
        #
        # ('PARKS_NON_PUBLIC', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 137,
        #     'code': 5900,
        #     'county': 'nassau',
        #     'rule_name': '4-Parks - Non public',
        # }),
        #
        # ('PLAYGROUNDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 138,
        #     'code': 5910,
        #     'county': 'nassau',
        #     'rule_name': '4-Playgrounds',
        # }),
        #
        # ('ATHLETIC_FIELDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 139,
        #     'code': 5920,
        #     'county': 'nassau',
        #     'rule_name': '4-Athletic Fields',
        # }),
        #
        # ('RELIGIOUS_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 140,
        #     'code': 6001,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious - Other',
        # }),
        #
        # ('RELIGIOUS_OTHER_2', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 141,
        #     'code': 6002,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious - Other - 2',
        # }),
        #
        # ('RELIGIOUS_PARKING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 142,
        #     'code': 6008,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious - Parking',
        # }),
        #
        # ('LONG_ISLAND_RAILROAD', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 143,
        #     'code': 6009,
        #     'county': 'nassau',
        #     'rule_name': '4-Long Island Railroad',
        # }),
        #
        # ('EDUCATION', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 144,
        #     'code': 6100,
        #     'county': 'nassau',
        #     'rule_name': '4-Education',
        # }),
        #
        # ('LIBRARIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 145,
        #     'code': 6110,
        #     'county': 'nassau',
        #     'rule_name': '4-Libraries',
        # }),
        #
        # ('LIBRARY_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 146,
        #     'code': 6111,
        #     'county': 'nassau',
        #     'rule_name': '4 -Library - Other',
        # }),
        #
        # ('SCHOOLS_PUBLIC', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 147,
        #     'code': 6121,
        #     'county': 'nassau',
        #     'rule_name': '4-Schools - Public',
        # }),
        #
        # ('SCHOOLS_TUITION_CHARGED', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 148,
        #     'code': 6122,
        #     'county': 'nassau',
        #     'rule_name': '4-Schools - Tuition Charged',
        # }),
        #
        # ('COLLEGES_AND_UNIVERITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 149,
        #     'code': 6130,
        #     'county': 'nassau',
        #     'rule_name': '4-Colleges and Universities',
        # }),
        #
        # ('SPECIAL_ED_SCHOOLS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 150,
        #     'code': 6140,
        #     'county': 'nassau',
        #     'rule_name': '4-Special ED Schools',
        # }),
        #
        # ('OTHER_EDUCATIONAL_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 151,
        #     'code': 6150,
        #     'county': 'nassau',
        #     'rule_name': '4-Other Educational Facilities',
        # }),
        #
        # ('RELIGIOUS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 152,
        #     'code': 6200,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious',
        # }),
        #
        # ('RELIGIOUS_2', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 152,
        #     'code': 6201,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious-2',
        # }),
        #
        # ('RELIGIOUS_PARKING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 153,
        #     'code': 6208,
        #     'county': 'nassau',
        #     'rule_name': '4-Religious - Parking',
        # }),
        #
        # ('WELFARE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 154,
        #     'code': 6300,
        #     'county': 'nassau',
        #     'rule_name': '4-Welfare',
        # }),
        #
        # ('FRATERNAL_AND_BENEVOLENT_ASSOCIATIONS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 155,
        #     'code': 6321,
        #     'county': 'nassau',
        #     'rule_name': '4-Fraternal & Benevolent Associations',
        # }),
        #
        # ('HOME_FOR_AGES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 156,
        #     'code': 6330,
        #     'county': 'nassau',
        #     'rule_name': '4-Home for Ages',
        # }),
        #
        # ('HOSPITALS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 157,
        #     'code': 6410,
        #     'county': 'nassau',
        #     'rule_name': '4-Hospitals',
        # }),
        #
        # ('HOSPITAL_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 158,
        #     'code': 6411,
        #     'county': 'nassau',
        #     'rule_name': '4-Hospital - Other',
        # }),
        #
        # ('ALL_OTHER_HEALTH_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 159,
        #     'code': 6420,
        #     'county': 'nassau',
        #     'rule_name': '4-All Other Health Facilities',
        # }),
        #
        # ('GOVERNMENT_HIGHWAY_GARAGES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 160,
        #     'code': 6510,
        #     'county': 'nassau',
        #     'rule_name': '4-Government Highway Garages',
        # }),
        #
        # ('GOVERNMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 161,
        #     'code': 6515,
        #     'county': 'nassau',
        #     'rule_name': '4-Government',
        # }),
        #
        # ('GOVERNMENT_BUILDINGS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 162,
        #     'code': 6520,
        #     'county': 'nassau',
        #     'rule_name': '4-Government Buildings',
        # }),
        #
        # ('US_GOVERNMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 163,
        #     'code': 6521,
        #     'county': 'nassau',
        #     'rule_name': '4-US Government',
        # }),
        #
        # ('US_POST_OFFICE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 164,
        #     'code': 6522,
        #     'county': 'nassau',
        #     'rule_name': '4-US Post Office',
        # }),
        #
        # ('FOREIGN_GVERNMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 165,
        #     'code': 6523,
        #     'county': 'nassau',
        #     'rule_name': '4-Foreign Government',
        # }),
        #
        # ('PUBLIC_HOUSIG_PROJECTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 166,
        #     'code': 6524,
        #     'county': 'nassau',
        #     'rule_name': '4-Public Housing Projects',
        # }),
        #
        # ('NEW_YORK_STATE', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 167,
        #     'code': 6525,
        #     'county': 'nassau',
        #     'rule_name': '4-New York State',
        # }),
        #
        # ('NASSAU_COUNTY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 168,
        #     'code': 6526,
        #     'county': 'nassau',
        #     'rule_name': '4-Nassau County',
        # }),
        #
        # ('TOWN', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 169,
        #     'code': 6527,
        #     'county': 'nassau',
        #     'rule_name': '4-Town',
        # }),
        #
        # ('CITY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 170,
        #     'code': 6528,
        #     'county': 'nassau',
        #     'rule_name': '4-City',
        # }),
        #
        # ('VILLAGES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 171,
        #     'code': 6529,
        #     'county': 'nassau',
        #     'rule_name': '4-Villages',
        # }),
        #
        # ('GOVERNMENT_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 172,
        #     'code': 6530,
        #     'county': 'nassau',
        #     'rule_name': '4-Government Parking Lots',
        # }),
        #
        # ('FEDERAL_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 173,
        #     'code': 6531,
        #     'county': 'nassau',
        #     'rule_name': '4-Federal  Parking Lots',
        # }),
        #
        # ('STATE_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 174,
        #     'code': 6535,
        #     'county': 'nassau',
        #     'rule_name': '4-State  Parking Lots',
        # }),
        #
        # ('COUNTY_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 175,
        #     'code': 6536,
        #     'county': 'nassau',
        #     'rule_name': '4-County  Parking Lots',
        # }),
        #
        # ('TOWN_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 176,
        #     'code': 6537,
        #     'county': 'nassau',
        #     'rule_name': '4-Town  Parking Lots',
        # }),
        #
        # ('CITY_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 177,
        #     'code': 6538,
        #     'county': 'nassau',
        #     'rule_name': '4-City  Parking Lots',
        # }),
        #
        # ('VILLAGE_PARKING_LOTS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 178,
        #     'code': 6539,
        #     'county': 'nassau',
        #     'rule_name': '4-Village Parking Lots',
        # }),
        #
        # ('PROTECTION', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 179,
        #     'code': 6600,
        #     'county': 'nassau',
        #     'rule_name': '4-Protection',
        # }),
        #
        # ('POLICE_OR_FIRE_PROTECTION_SIGNAL_EQUIPMENT', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 180,
        #     'code': 6620,
        #     'county': 'nassau',
        #     'rule_name': '4-Police/Fire Protection, Signal Equipme',
        # }),
        #
        # ('POLICE_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 181,
        #     'code': 6621,
        #     'county': 'nassau',
        #     'rule_name': '4-Police - Other',
        # }),
        #
        # ('CORRECTIONAL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 182,
        #     'code': 6700,
        #     'county': 'nassau',
        #     'rule_name': '4-Correctional',
        # }),
        #
        # ('CULTURAL_AND_RECREATIONAL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 183,
        #     'code': 6800,
        #     'county': 'nassau',
        #     'rule_name': '4-Cultural and Recreational',
        # }),
        #
        # ('CULTURAL_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 184,
        #     'code': 6810,
        #     'county': 'nassau',
        #     'rule_name': '4-Cultural Facilities',
        # }),
        #
        # ('RECREATIONAL_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 185,
        #     'code': 6820,
        #     'county': 'nassau',
        #     'rule_name': '4-Recreational Facilitates',
        # }),
        #
        # ('MISCELLANEOUS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 186,
        #     'code': 6900,
        #     'county': 'nassau',
        #     'rule_name': '4-Miscellaneous',
        # }),
        #
        # ('PROF_ASSOC_NASSAU_COUNTY_BAR_ASSOC', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 187,
        #     'code': 6910,
        #     'county': 'nassau',
        #     'rule_name': '4-Prof Assoc, Nassau County Bar Assoc.',
        # }),
        #
        # ('ANIMAL_WELFARE_SHELTERS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 188,
        #     'code': 6940,
        #     'county': 'nassau',
        #     'rule_name': '4-Animal Welfare (shelters)',
        # }),
        #
        # ('CEMETERIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 189,
        #     'code': 6950,
        #     'county': 'nassau',
        #     'rule_name': '4-Cemeteries',
        # }),
        #
        # ('CEMETERIES_OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 190,
        #     'code': 6951,
        #     'county': 'nassau',
        #     'rule_name': '4-Cemeteries - Other',
        # }),
        #
        # ('MANUFACTURING_AND_PROCESSING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 192,
        #     'code': 7100,
        #     'county': 'nassau',
        #     'rule_name': '4-manufacturing and Processing',
        # }),
        #
        # ('HEAVY_MANUFACTURING_FACTORY_COMPLEX', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 193,
        #     'code': 7101,
        #     'county': 'nassau',
        #     'rule_name': '4-Heavy Manufacturing, Factory Complex',
        # }),
        #
        # ('LIGHT_MANUFACTURING_SMALL_FACTORY_BLD', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 194,
        #     'code': 7102,
        #     'county': 'nassau',
        #     'rule_name': '4-Light Manufacturing, Small Factory Bld',
        # }),
        #
        # ('JOB_SHOPS_AND_MULTIPLE_USE_BUILDING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 195,
        #     'code': 7103,
        #     'county': 'nassau',
        #     'rule_name': '4-Job Shops and Multiple Use Building',
        # }),
        #
        # ('SMALL_IMPROVEMENTS_USED_WITH_FACILITIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 196,
        #     'code': 7107,
        #     'county': 'nassau',
        #     'rule_name': '4-Small Improvements used with Factories',
        # }),
        #
        # ('PAVING_FENCING_USED_FOR_FACTORIES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 197,
        #     'code': 7108,
        #     'county': 'nassau',
        #     'rule_name': '4-Paving, Fencing used for Factories',
        # }),
        #
        # ('HI_TECH_MANUFACTURING', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 198,
        #     'code': 7120,
        #     'county': 'nassau',
        #     'rule_name': '4-Hi Tech Manufacturing',
        # }),
        #
        # ('SAND_AND_GRAVEL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 199,
        #     'code': 7210,
        #     'county': 'nassau',
        #     'rule_name': '4-Sand and Gravel',
        # }),
        #
        # ('OTHER', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 200,
        #     'code': 7290,
        #     'county': 'nassau',
        #     'rule_name': '4-Other',
        # }),
        #
        # ('OTHER_2', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 201,
        #     'code': 8010,
        #     'county': 'nassau',
        #     'rule_name': '4-Other-2',
        # }),
        #
        # ('OTHER_3', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 202,
        #     'code': 8020,
        #     'county': 'nassau',
        #     'rule_name': '4-Other-3',
        # }),
        #
        # ('ELECTRIC_POWER_GENERATION_GAS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 203,
        #     'code': 8150,
        #     'county': 'nassau',
        #     'rule_name': '4-Electric Power Generation - Gas',
        # }),
        #
        # ('ELECTRIC_POWER_GENERATION_GAS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 203,
        #     'code': 8150,
        #     'county': 'nassau',
        #     'rule_name': '4-Electric Power Generation - Gas',
        # }),
        #
        # ('WATER_OBS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 204,
        #     'code': 8200,
        #     'county': 'nassau',
        #     'rule_name': '4-Water',
        # }),
        #
        # ('WATER_SUPPLY', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 205,
        #     'code': 8220,
        #     'county': 'nassau',
        #     'rule_name': '4-Water Supply',
        # }),
        #
        # ('TELECOMMUNICATIONS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 206,
        #     'code': 8360,
        #     'county': 'nassau',
        #     'rule_name': '3-Telecommunications',
        # }),
        #
        # ('MOTOR_VEHICLE_TRANSPORTATION_SERVICES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 207,
        #     'code': 8411,
        #     'county': 'nassau',
        #     'rule_name': '4-Motor Vehicle Transportation Services',
        # }),
        #
        # ('SEWAGE_AND_WATER_POLLUTION_CONTROL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 208,
        #     'code': 8530,
        #     'county': 'nassau',
        #     'rule_name': "4-Sewage and Water Pollution's Control",
        # }),
        #
        # ('PRIVATE_WILD_AND_FOREST_LANDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 209,
        #     'code': 9100,
        #     'county': 'nassau',
        #     'rule_name': "4-Private, Wild and Forest Lands",
        # }),
        #
        # ('HUNTNG_AND_FISHING_CLUBS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 210,
        #     'code': 9201,
        #     'county': 'nassau',
        #     'rule_name': "4-Hunting and Fishing Clubs",
        # }),
        #
        # ('STATE_OWNED_LANDS_OTHER_THAT_FOREST', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 211,
        #     'code': 9320,
        #     'county': 'nassau',
        #     'rule_name': "4-State Owned lands other that Forest",
        # }),
        #
        # ('LAND_FOR_CONSERVATION_PURPOSES', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 212,
        #     'code': 9400,
        #     'county': 'nassau',
        #     'rule_name': "4-Land for Conservation Purposes",
        # }),
        #
        # ('PUBLIC_PARKS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 213,
        #     'code': 9600,
        #     'county': 'nassau',
        #     'rule_name': "4-Public Parks",
        # }),
        #
        # ('STATE_OWNED_PUBLIC_PARKS_AND_REC_AREAS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 214,
        #     'code': 9610,
        #     'county': 'nassau',
        #     'rule_name': "4-State Owned Public Parks and Rec Areas",
        # }),
        #
        # ('COUNTY_OWNED_PUBLIC_PARKS_AND_REC_AREA', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 215,
        #     'code': 9620,
        #     'county': 'nassau',
        #     'rule_name': "4-County Owned Public Parks and Rec Area",
        # }),
        #
        # ('CITY_OWED_PUBLIC_PARKS_AND_REC_AREAS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 216,
        #     'code': 9631,
        #     'county': 'nassau',
        #     'rule_name': "4-City Owed Public Parks and Rec Areas",
        # }),
        #
        # ('TOWN_OWED_PUBLIC_PARKS_AND_REC_AREAS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 217,
        #     'code': 9632,
        #     'county': 'nassau',
        #     'rule_name': "4-Town Owed Public Parks and Rec Areas",
        # }),
        #
        # ('VILLAGE_OWED_PUBLIC_PARKS_AND_REC_AREA', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 218,
        #     'code': 9633,
        #     'county': 'nassau',
        #     'rule_name': "4-Village Owed Public Parks and Rec Area",
        # }),
        #
        # ('ALL_OTHER_WILD_OR_CONSERVATION_LANDS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 219,
        #     'code': 9700,
        #     'county': 'nassau',
        #     'rule_name': "4-All Other Wild or Conservation Lands",
        # }),
        #
        # ('WETLANDS_SPECIFIC_USE_RESTRICTIONS', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 220,
        #     'code': 9710,
        #     'county': 'nassau',
        #     'rule_name': "4-Wetlands-Specific Use Restrictions",
        # }),
        #
        # ('LAND_UNDER_WATER_NON_RESIDENTIAL', {
        #     'rule_type': RULE_OBSOLESCENCE,
        #     'rule_index': 221,
        #     'code': 9720,
        #     'county': 'nassau',
        #     'rule_name': "4-Land under Water - non-residential",
        # }),

        # road obsolescenses
        ('BRIDLEWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 34,
            'code': 1000,
            'county': 'nassau',
            'rule_name': 'Bridleway',
        }),
        ('CONSTRUCTION', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 35,
            'code': 1001,
            'county': 'nassau',
            'rule_name': 'Construction',
        }),
        ('MOTORWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 36,
            'code': 1002,
            'county': 'nassau',
            'rule_name': 'Motorway',
        }),
        ('MOTORWAY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 37,
            'code': 1003,
            'county': 'nassau',
            'rule_name': 'Motorway Link',
        }),
        ('PRIMARY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 38,
            'code': 1004,
            'county': 'nassau',
            'rule_name': 'Primary',
        }),
        ('PRIMARY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 39,
            'code': 1005,
            'county': 'nassau',
            'rule_name': 'Primary Link',
        }),
        ('RACEWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 40,
            'code': 1006,
            'county': 'nassau',
            'rule_name': 'Raceway',
        }),
        ('SECONDAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 41,
            'code': 1007,
            'county': 'nassau',
            'rule_name': 'Secondary',
        }),
        ('SECONDAY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 42,
            'code': 1008,
            'county': 'nassau',
            'rule_name': 'Secondary Link',
        }),
        ('TERTIARY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 43,
            'code': 1009,
            'county': 'nassau',
            'rule_name': 'Tertiary',
        }),
        ('TERTIARY_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 44,
            'code': 1010,
            'county': 'nassau',
            'rule_name': 'Tertiary Link',
        }),
        ('TRACK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 45,
            'code': 1011,
            'county': 'nassau',
            'rule_name': 'Track',
        }),
        ('TRUNK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 46,
            'code': 1012,
            'county': 'nassau',
            'rule_name': 'Trunk',
        }),
        ('TRUNK_LINK', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 47,
            'code': 1013,
            'county': 'nassau',
            'rule_name': 'Trunk Link',
        }),
        ('RAILWAY', {
            'rule_type': RULE_OBSOLESCENCE,
            'rule_index': 48,
            'code': 1014,
            'county': 'nassau',
            'rule_name': 'Railway',
        }),
    ]),
    'suffolk': OrderedDict(),
    'broward': get_florida_obsolescence('broward'),
    'miamidade': get_florida_obsolescence('miamidade'),
    'palmbeach': get_florida_obsolescence('palmbeach')
}


def simplify_obsolescence(county, code):
    # code: is a property of a property...present in db as separate column in
    # property table.
    # TODO: adjust for other counties beside nassau
    if county == 'nassau':
        mapper = OBSOLESCENCE_SIMPLIFY_MAPPER.get(county)
        # this column can be found in obsolescence chart.xls file
        county_code = mapper.get(code)
        return county_code

    else:
        # for now implemented only for nassau
        return code


def get_value_from_code(county, code):
    # simplify the code
    code = simplify_obsolescence(county, code)
    if not code:
        return None

    obs_rules = ALL_OBSOLESCENCE.get(county)
    vals = obs_rules.values()
    filtered = [val for val in vals if val['code'] == code]

    if filtered:
        return filtered[0]
    return None


def get_code_from_name(county, name):
    # for nassau only
    if county == 'nassau':
        mapper = OBSOLESCENCE_SIMPLIFY_MAPPER.get(county)
        return mapper[name]
    else:
        # TODO: this else statement is temp. As soon as we get mapper for
        # rest of the counties, this else statement has to be adjusted to
        # look like the if statement
        obs_rules = ALL_OBSOLESCENCE.get(county)
        vals = obs_rules.values()
        filtered = [val for val in vals if val['rule_name'].lower().replace(' ', '_') == name]
        if filtered:
            return filtered[0]['code']
        return None


def get_code_from_idx(county, idx):
    obs_rules = ALL_OBSOLESCENCE.get(county)
    vals = obs_rules.values()
    filtered = [val for val in vals if val['rule_index'] == idx]
    if filtered:
        return filtered[0]['code']
    return None


def get_index_from_code(county, code):
    value = get_value_from_code(county, code)
    if value:
        return value['rule_index']
    return None


def get_name_from_code(county, code):
    value = get_value_from_code(county, code)
    if value:
        return value['rule_name']
    return None
