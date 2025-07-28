# flake8: noqa
from collections import namedtuple
from uuid import uuid4

import click
from flask import Blueprint, current_app
from psycopg2.extras import execute_values
from sqlalchemy.exc import InternalError
from tqdm import tqdm

from app import db, create_app
from app.database.models import Property
from app.database.models.property import Road
from app.utils.constants import County

bp = Blueprint('obsolescence', __name__)

app = create_app()
app.app_context().push()


class ObsFilter:
    def __init__(self, obs_properties,
                 surrounding_properties, road_types):
        self.obs_properties = obs_properties
        self.surrounding_properties = surrounding_properties
        self.road_types = road_types


COUNTY_FILTERS = {
    County.NASSAU:
        ObsFilter(obs_properties='''
    AND (property_class = 1120 AND property_class_type = 4)
   OR (property_class = 1170 AND property_class_type = 4)
   OR (property_class = 1200 AND property_class_type = 4)
   OR (property_class = 1400 AND property_class_type = 4)
   OR (property_class = 1700 AND property_class_type = 4)
   OR (property_class = 2800 AND property_class_type = 2)
   OR (property_class = 3121 AND property_class_type = 1)
   OR (property_class = 3140 AND property_class_type = 4)
   OR (property_class = 3150 AND property_class_type = 1)
   OR (property_class = 3150 AND property_class_type = 4)
   OR (property_class = 3160 AND property_class_type = 1)
   OR (property_class = 3160 AND property_class_type = 4)
   OR (property_class = 4001 AND property_class_type = 4)
   OR (property_class = 4002 AND property_class_type = 4)
   OR (property_class = 4108 AND property_class_type = 4)
   OR (property_class = 4110 AND property_class_type = 2)
   OR (property_class = 4111 AND property_class_type = 2)
   OR (property_class = 4112 AND property_class_type = 2)
   OR (property_class = 4116 AND property_class_type = 2)
   OR (property_class = 4117 AND property_class_type = 2)
   OR (property_class = 4118 AND property_class_type = 2)
   OR (property_class = 4121 AND property_class_type = 2)
   OR (property_class = 4127 AND property_class_type = 2)
   OR (property_class = 4127 AND property_class_type = 4)
   OR (property_class = 4131 AND property_class_type = 2)
   OR (property_class = 4137 AND property_class_type = 2)
   OR (property_class = 4138 AND property_class_type = 2)
   OR (property_class = 4141 AND property_class_type = 4)
   OR (property_class = 4151 AND property_class_type = 4)
   OR (property_class = 4181 AND property_class_type = 4)
   OR (property_class = 4200 AND property_class_type = 4)
   OR (property_class = 4207 AND property_class_type = 4)
   OR (property_class = 4208 AND property_class_type = 4)
   OR (property_class = 4211 AND property_class_type = 4)
   OR (property_class = 4221 AND property_class_type = 4)
   OR (property_class = 4231 AND property_class_type = 4)
   OR (property_class = 4241 AND property_class_type = 4)
   OR (property_class = 4251 AND property_class_type = 4)
   OR (property_class = 4261 AND property_class_type = 4)
   OR (property_class = 4300 AND property_class_type = 4)
   OR (property_class = 4307 AND property_class_type = 4)
   OR (property_class = 4308 AND property_class_type = 4)
   OR (property_class = 4311 AND property_class_type = 4)
   OR (property_class = 4312 AND property_class_type = 4)
   OR (property_class = 4321 AND property_class_type = 4)
   OR (property_class = 4322 AND property_class_type = 4)
   OR (property_class = 4323 AND property_class_type = 4)
   OR (property_class = 4324 AND property_class_type = 4)
   OR (property_class = 4331 AND property_class_type = 4)
   OR (property_class = 4341 AND property_class_type = 4)
   OR (property_class = 4350 AND property_class_type = 4)
   OR (property_class = 4360 AND property_class_type = 4)
   OR (property_class = 4371 AND property_class_type = 4)
   OR (property_class = 4371 AND property_class_type = 2)
   OR (property_class = 4380 AND property_class_type = 4)
   OR (property_class = 4390 AND property_class_type = 4)
   OR (property_class = 4400 AND property_class_type = 4)
   OR (property_class = 4408 AND property_class_type = 4)
   OR (property_class = 4411 AND property_class_type = 4)
   OR (property_class = 4420 AND property_class_type = 4)
   OR (property_class = 4421 AND property_class_type = 4)
   OR (property_class = 4441 AND property_class_type = 4)
   OR (property_class = 4451 AND property_class_type = 4)
   OR (property_class = 4461 AND property_class_type = 4)
   OR (property_class = 4471 AND property_class_type = 4)
   OR (property_class = 4480 AND property_class_type = 4)
   OR (property_class = 4490 AND property_class_type = 4)
   OR (property_class = 4500 AND property_class_type = 4)
   OR (property_class = 4502 AND property_class_type = 4)
   OR (property_class = 4507 AND property_class_type = 4)
   OR (property_class = 4508 AND property_class_type = 4)
   OR (property_class = 4511 AND property_class_type = 4)
   OR (property_class = 4521 AND property_class_type = 4)
   OR (property_class = 4522 AND property_class_type = 4)
   OR (property_class = 4531 AND property_class_type = 4)
   OR (property_class = 4532 AND property_class_type = 4)
   OR (property_class = 4540 AND property_class_type = 4)
   OR (property_class = 4550 AND property_class_type = 4)
   OR (property_class = 4600 AND property_class_type = 4)
   OR (property_class = 4607 AND property_class_type = 4)
   OR (property_class = 4608 AND property_class_type = 4)
   OR (property_class = 4611 AND property_class_type = 4)
   OR (property_class = 4621 AND property_class_type = 4)
   OR (property_class = 4631 AND property_class_type = 4)
   OR (property_class = 4641 AND property_class_type = 4)
   OR (property_class = 4642 AND property_class_type = 4)
   OR (property_class = 4651 AND property_class_type = 4)
   OR (property_class = 4652 AND property_class_type = 4)
   OR (property_class = 4653 AND property_class_type = 4)
   OR (property_class = 4654 AND property_class_type = 4)
   OR (property_class = 4711 AND property_class_type = 4)
   OR (property_class = 4717 AND property_class_type = 4)
   OR (property_class = 4718 AND property_class_type = 4)
   OR (property_class = 4721 AND property_class_type = 4)
   OR (property_class = 4728 AND property_class_type = 4)
   OR (property_class = 4731 AND property_class_type = 4)
   OR (property_class = 4737 AND property_class_type = 4)
   OR (property_class = 4738 AND property_class_type = 4)
   OR (property_class = 4751 AND property_class_type = 4)
   OR (property_class = 4800 AND property_class_type = 4)
   OR (property_class = 4801 AND property_class_type = 4)
   OR (property_class = 4801 AND property_class_type = 2)
   OR (property_class = 4807 AND property_class_type = 4)
   OR (property_class = 4808 AND property_class_type = 4)
   OR (property_class = 4811 AND property_class_type = 4)
   OR (property_class = 4811 AND property_class_type = 2)
   OR (property_class = 4821 AND property_class_type = 4)
   OR (property_class = 4822 AND property_class_type = 4)
   OR (property_class = 4830 AND property_class_type = 4)
   OR (property_class = 4831 AND property_class_type = 4)
   OR (property_class = 4832 AND property_class_type = 4)
   OR (property_class = 4841 AND property_class_type = 4)
   OR (property_class = 4851 AND property_class_type = 4)
   OR (property_class = 4861 AND property_class_type = 4)
   OR (property_class = 5100 AND property_class_type = 4)
   OR (property_class = 5107 AND property_class_type = 4)
   OR (property_class = 5108 AND property_class_type = 4)
   OR (property_class = 5121 AND property_class_type = 4)
   OR (property_class = 5140 AND property_class_type = 4)
   OR (property_class = 5151 AND property_class_type = 4)
   OR (property_class = 5221 AND property_class_type = 4)
   OR (property_class = 5300 AND property_class_type = 4)
   OR (property_class = 5321 AND property_class_type = 4)
   OR (property_class = 5341 AND property_class_type = 4)
   OR (property_class = 5400 AND property_class_type = 4)
   OR (property_class = 5411 AND property_class_type = 4)
   OR (property_class = 5421 AND property_class_type = 4)
   OR (property_class = 5431 AND property_class_type = 4)
   OR (property_class = 5441 AND property_class_type = 4)
   OR (property_class = 5450 AND property_class_type = 4)
   OR (property_class = 5461 AND property_class_type = 4)
   OR (property_class = 5520 AND property_class_type = 4)
   OR (property_class = 5531 AND property_class_type = 4)
   OR (property_class = 5541 AND property_class_type = 4)
   OR (property_class = 5551 AND property_class_type = 4)
   OR (property_class = 5560 AND property_class_type = 4)
   OR (property_class = 5570 AND property_class_type = 4)
   OR (property_class = 5600 AND property_class_type = 4)
   OR (property_class = 5601 AND property_class_type = 4)
   OR (property_class = 5700 AND property_class_type = 4)
   OR (property_class = 5701 AND property_class_type = 4)
   OR (property_class = 5702 AND property_class_type = 4)
   OR (property_class = 5703 AND property_class_type = 4)
   OR (property_class = 5704 AND property_class_type = 4)
   OR (property_class = 5705 AND property_class_type = 4)
   OR (property_class = 5810 AND property_class_type = 4)
   OR (property_class = 5830 AND property_class_type = 4)
   OR (property_class = 5900 AND property_class_type = 4)
   OR (property_class = 5910 AND property_class_type = 4)
   OR (property_class = 5920 AND property_class_type = 4)
   OR (property_class = 6001 AND property_class_type = 4)
   OR (property_class = 6002 AND property_class_type = 4)
   OR (property_class = 6008 AND property_class_type = 4)
   OR (property_class = 6009 AND property_class_type = 4)
   OR (property_class = 6100 AND property_class_type = 4)
   OR (property_class = 6110 AND property_class_type = 1)
   OR (property_class = 6110 AND property_class_type = 4)
   OR (property_class = 6111 AND property_class_type = 4)
   OR (property_class = 6121 AND property_class_type = 4)
   OR (property_class = 6121 AND property_class_type = 1)
   OR (property_class = 6122 AND property_class_type = 1)
   OR (property_class = 6122 AND property_class_type = 4)
   OR (property_class = 6130 AND property_class_type = 1)
   OR (property_class = 6130 AND property_class_type = 4)
   OR (property_class = 6140 AND property_class_type = 4)
   OR (property_class = 6140 AND property_class_type = 1)
   OR (property_class = 6150 AND property_class_type = 1)
   OR (property_class = 6150 AND property_class_type = 4)
   OR (property_class = 6200 AND property_class_type = 1)
   OR (property_class = 6200 AND property_class_type = 4)
   OR (property_class = 6201 AND property_class_type = 1)
   OR (property_class = 6201 AND property_class_type = 4)
   OR (property_class = 6208 AND property_class_type = 4)
   OR (property_class = 6300 AND property_class_type = 4)
   OR (property_class = 6321 AND property_class_type = 1)
   OR (property_class = 6321 AND property_class_type = 4)
   OR (property_class = 6330 AND property_class_type = 4)
   OR (property_class = 6410 AND property_class_type = 4)
   OR (property_class = 6410 AND property_class_type = 1)
   OR (property_class = 6411 AND property_class_type = 4)
   OR (property_class = 6420 AND property_class_type = 1)
   OR (property_class = 6420 AND property_class_type = 4)
   OR (property_class = 6510 AND property_class_type = 4)
   OR (property_class = 6515 AND property_class_type = 4)
   OR (property_class = 6520 AND property_class_type = 4)
   OR (property_class = 6521 AND property_class_type = 4)
   OR (property_class = 6521 AND property_class_type = 1)
   OR (property_class = 6522 AND property_class_type = 4)
   OR (property_class = 6523 AND property_class_type = 1)
   OR (property_class = 6524 AND property_class_type = 1)
   OR (property_class = 6524 AND property_class_type = 2)
   OR (property_class = 6524 AND property_class_type = 4)
   OR (property_class = 6525 AND property_class_type = 1)
   OR (property_class = 6525 AND property_class_type = 2)
   OR (property_class = 6525 AND property_class_type = 4)
   OR (property_class = 6526 AND property_class_type = 1)
   OR (property_class = 6526 AND property_class_type = 2)
   OR (property_class = 6526 AND property_class_type = 4)
   OR (property_class = 6527 AND property_class_type = 1)
   OR (property_class = 6527 AND property_class_type = 2)
   OR (property_class = 6527 AND property_class_type = 4)
   OR (property_class = 6528 AND property_class_type = 1)
   OR (property_class = 6528 AND property_class_type = 2)
   OR (property_class = 6528 AND property_class_type = 4)
   OR (property_class = 6529 AND property_class_type = 1)
   OR (property_class = 6529 AND property_class_type = 4)
   OR (property_class = 6530 AND property_class_type = 4)
   OR (property_class = 6531 AND property_class_type = 4)
   OR (property_class = 6535 AND property_class_type = 4)
   OR (property_class = 6536 AND property_class_type = 4)
   OR (property_class = 6537 AND property_class_type = 4)
   OR (property_class = 6538 AND property_class_type = 4)
   OR (property_class = 6539 AND property_class_type = 4)
   OR (property_class = 6600 AND property_class_type = 1)
   OR (property_class = 6620 AND property_class_type = 1)
   OR (property_class = 6620 AND property_class_type = 4)
   OR (property_class = 6621 AND property_class_type = 4)
   OR (property_class = 6700 AND property_class_type = 4)
   OR (property_class = 6800 AND property_class_type = 1)
   OR (property_class = 6800 AND property_class_type = 4)
   OR (property_class = 6810 AND property_class_type = 4)
   OR (property_class = 6810 AND property_class_type = 1)
   OR (property_class = 6820 AND property_class_type = 1)
   OR (property_class = 6820 AND property_class_type = 4)
   OR (property_class = 6900 AND property_class_type = 1)
   OR (property_class = 6910 AND property_class_type = 4)
   OR (property_class = 6940 AND property_class_type = 1)
   OR (property_class = 6940 AND property_class_type = 4)
   OR (property_class = 6950 AND property_class_type = 1)
   OR (property_class = 6950 AND property_class_type = 4)
   OR (property_class = 6951 AND property_class_type = 4)
   OR (property_class = 7100 AND property_class_type = 4)
   OR (property_class = 7101 AND property_class_type = 4)
   OR (property_class = 7102 AND property_class_type = 4)
   OR (property_class = 7103 AND property_class_type = 4)
   OR (property_class = 7107 AND property_class_type = 4)
   OR (property_class = 7108 AND property_class_type = 4)
   OR (property_class = 7120 AND property_class_type = 4)
   OR (property_class = 7210 AND property_class_type = 4)
   OR (property_class = 7290 AND property_class_type = 4)
   OR (property_class = 8010 AND property_class_type = 4)
   OR (property_class = 8020 AND property_class_type = 4)
   OR (property_class = 8150 AND property_class_type = 4)
   OR (property_class = 8200 AND property_class_type = 4)
   OR (property_class = 8220 AND property_class_type = 4)
   OR (property_class = 8360 AND property_class_type = 4)
   OR (property_class = 8411 AND property_class_type = 4)
   OR (property_class = 8530 AND property_class_type = 4)
   OR (property_class = 9100 AND property_class_type = 4)
   OR (property_class = 9201 AND property_class_type = 4)
   OR (property_class = 9320 AND property_class_type = 4)
   OR (property_class = 9400 AND property_class_type = 4)
   OR (property_class = 9600 AND property_class_type = 4)
   OR (property_class = 9610 AND property_class_type = 4)
   OR (property_class = 9610 AND property_class_type = 1)
   OR (property_class = 9620 AND property_class_type = 1)
   OR (property_class = 9620 AND property_class_type = 4)
   OR (property_class = 9631 AND property_class_type = 4)
   OR (property_class = 9632 AND property_class_type = 1)
   OR (property_class = 9632 AND property_class_type = 4)
   OR (property_class = 9633 AND property_class_type = 1)
   OR (property_class = 9633 AND property_class_type = 4)
   OR (property_class = 9700 AND property_class_type = 4)
   OR (property_class = 9710 AND property_class_type = 4)
   OR (property_class = 9720 AND property_class_type = 4)
        ''',
                  surrounding_properties='''
    AND NOT ((property_class = 3009 AND property_class_type = 1)
   OR (property_class = 3009 AND property_class_type = 4)
   OR (property_class = 3111 AND property_class_type = 1)
   OR (property_class = 3130 AND property_class_type = 1)
   OR (property_class = 3130 AND property_class_type = 2)
   OR (property_class = 3130 AND property_class_type = 4)
   OR (property_class = 3220 AND property_class_type = 1)
   OR (property_class = 3230 AND property_class_type = 1)
   OR (property_class = 3230 AND property_class_type = 4)
   OR (property_class = 3301 AND property_class_type = 4)
   OR (property_class = 3401 AND property_class_type = 4)
   OR (property_class = 6920 AND property_class_type = 1)
   OR (property_class = 6920 AND property_class_type = 4))
                  ''',
                  road_types="('bridleway','construction',"
                             "'motorway','motorway_link',"
                             "'primary','primary_link','raceway',"
                             "'secondary','secondary_link',"
                             "'tertiary','tertiary_link','track','trunk','trunk_link', 'railway')"
    ),
    County.SUFFOLK:
        ObsFilter(obs_properties='''
    AND property_class IN
      (105, 110, 111, 112, 113, 114, 115, 116, 117, 120, 129, 130, 140, 150, 151, 152, 160, 170, 180, 181, 182, 183,
       184, 190, 410, 411, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 430, 431, 432, 433, 434, 435,
       436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 460, 461,
       462, 463, 464, 465, 470, 471, 472, 473, 474, 475, 480, 481, 482, 484, 485, 486, 510, 511, 512, 513, 514, 515,
       520, 521, 522, 530, 531, 532, 533, 534, 540, 541, 542, 543, 544, 545, 546, 550, 551, 552, 553, 554, 555, 556,
       557, 560, 570, 580, 581, 582, 583, 590, 591, 592, 593, 610, 611, 612, 613, 614, 615, 620, 630, 631, 632, 633,
       640, 641, 642, 650, 651, 652, 653, 660, 661, 662, 670, 680, 681, 682, 690, 691, 692, 693, 694, 695, 710, 712,
       714, 715, 720, 721, 722, 723, 724, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 740, 741, 742, 743,
       744, 749, 810, 811, 812, 813, 814, 815, 816, 817, 818, 820, 821, 822, 823, 826, 827, 830, 831, 832, 833, 834,
       835, 836, 837, 840, 841, 842, 843, 844, 845, 846, 847, 850, 851, 852, 853, 854, 860, 861, 862, 866, 867, 868,
       869, 870, 871, 872, 873, 874, 875, 876, 877, 880, 882, 883, 884, 885, 900, 910, 911, 912, 920, 930, 931, 932,
       940, 941, 942, 950, 960, 961, 962, 963, 970, 971, 972, 980, 990, 991, 992, 993, 994)
        ''',
                  surrounding_properties='''
    AND property_class not IN
      (310, 311, 312, 313, 314, 315, 316, 320, 321, 322, 323, 330, 331, 340, 341, 350, 351, 352, 380)
                  ''',
                  road_types="('bridleway','construction',"
                             "'motorway','motorway_link',"
                             "'primary','primary_link','raceway',"
                             "'secondary','secondary_link',"
                             "'tertiary','tertiary_link','track','trunk','trunk_link', 'railway')"
    ),
    County.MIAMIDADE:
        ObsFilter(obs_properties='and land_use in (3, 10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,'
                                 '19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,'
                                 '29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,'
                                 '39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,'
                                 '49 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,'
                                 '79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89, 96)',
                  surrounding_properties='and property.land_use not in (0,9,10,40,70,80,94,95)',
                  road_types="('bridleway','construction',"
                             "'motorway','motorway_link',"
                             "'primary','primary_link','raceway',"
                             "'secondary','secondary_link',"
                             "'tertiary','tertiary_link','track','trunk','trunk_link', 'railway')"
                  ),
    County.BROWARD:
        ObsFilter(obs_properties='and land_use in (3, 10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,'
                                 '19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,'
                                 '29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,'
                                 '39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,'
                                 '49 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,'
                                 '79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89, 96)',
                  surrounding_properties='and property.land_use not in (0,9,10,40,70,80,94,95)',
                  road_types="('bridleway','construction',"
                             "'motorway','motorway_link',"
                             "'primary','primary_link','raceway',"
                             "'secondary','secondary_link',"
                             "'tertiary','tertiary_link','track','trunk','trunk_link', 'railway')"
                  ),
    County.PALMBEACH:
        ObsFilter(obs_properties='and land_use in (3, 10 ,11 ,12 ,13 ,14 ,15 ,16 ,17 ,18 ,'
                                 '19 ,20 ,21 ,22 ,23 ,24 ,25 ,26 ,27 ,28 ,'
                                 '29 ,30 ,31 ,32 ,33 ,34 ,35 ,36 ,37 ,38 ,'
                                 '39 ,40 ,41 ,42 ,43 ,44 ,45 ,46 ,47 ,48 ,'
                                 '49 ,70 ,71 ,72 ,73 ,74 ,75 ,76 ,77 ,78 ,'
                                 '79 ,80 ,81 ,82 ,83 ,84 ,85 ,86 ,87 ,88 ,89, 96)',
                  surrounding_properties='and property.land_use not in (0,9,10,40,70,80,94,95)',
                  road_types="('bridleway','construction',"
                             "'motorway','motorway_link',"
                             "'primary','primary_link','raceway',"
                             "'secondary','secondary_link',"
                             "'tertiary','tertiary_link','track','trunk','trunk_link', 'railway')"
                  ),
}


@bp.cli.command('stop')
def stop_jobs():
    current_app.task_queue.delete(delete_jobs=True)


@bp.cli.command('compute')
@click.argument('county')
def compute_county(county):
    total = db.session.execute(f'''

        SELECT count(*)
        FROM property
        WHERE county = '{county}'
          AND id NOT IN (SELECT DISTINCT obs_id FROM obsolescences)
          and id not in (select DISTINCT property_id from helper.obsolescence)
          {COUNTY_FILTERS.get(county).obs_properties}
          and (geo notnull
          or reference_building notnull);
''').fetchone()[0]

    obs_properties = db.session.execute(f'''
        SELECT id, land_use, geo, reference_building
        FROM property
        WHERE county = '{county}'
          AND id NOT IN (SELECT DISTINCT obs_id FROM obsolescences)
          and id not in (select DISTINCT property_id from helper.obsolescence)
          {COUNTY_FILTERS.get(county).obs_properties}
          and (geo notnull
          or reference_building notnull);
    ''')

    count = 1
    for obs in obs_properties:
        property_id = obs[0]
        geo = obs[2]
        reference_building = obs[3]
        current_app.task_queue.enqueue(compute, property_id, geo, reference_building,
                                       county, count, total,
                                       job_timeout=2500)
        count += 1
        # if count == 20:
        #     return


@bp.cli.command('compute_single')
@click.argument('property_id')
def compute_single(property_id):
    prop = Property.query.get(property_id)
    compute(property_id, prop.geo, prop.reference_building, prop.county, 1, 1)


@bp.cli.command('compute_multiple')
@click.argument('property_ids', nargs=-1)
def compute_multiple(property_ids):
    """may be not working"""
    props = Property.query.filter(Property.id.in_(property_ids))
    for prop in props:
        current_app.task_queue.enqueue(compute, prop.id, prop.geo, prop.reference_building, prop.county,
                                       job_timeout=2000)


def compute(property_id, geo, reference_building, county, count, total,
            distance_between_points=5, min_seen_amount=2, how_far=100):
    """
    distance_between_points: distance between equidistant points. In algorithm we use number of points
    along perimeter. We calculate this value with perimeter length / distance_between_points
    min_seen_amount: the minimum amount of times property has to be seen from all points
    how_far: set the max distance from obsolescence to the properties

    examples:
    3659249 miamidade with no props within 100 meters
    703350 should return 135 affected props
    3078487 property with reference building
    """
    raw_point = "ST_GeomFromEWKB('\\x{}'::bytea)"

    with db.engine.connect() as con:
        # get all property_gis records related to property_id
        query = con.execute(f'''
        SELECT property_id, county, geometry
        FROM property_gis
        WHERE property_id = {property_id}
        ''').fetchall()

        if not query:
            if not reference_building:
                return
            query = con.execute(f'''
                    SELECT property_id, county, geometry
                    FROM property_gis
                    WHERE property_id = {reference_building}
                    ''').fetchall()
            if not query:
                con.execute(f'''
                insert into helper.obsolescence(property_id)
                VALUES ({property_id});
                ''')
                return

        unique_id = uuid4().hex  # hex removes the dashes
        buildings_crop = f'buildings_crop{unique_id}'
        within_100m_props = f'within_100m_props_{unique_id}'
        obs = f'obs{unique_id}'

        # create temp tables and functions
        con.execute('''
        DO $$
        BEGIN
        
            IF NOT EXISTS(
                SELECT schema_name
                  FROM information_schema.schemata
                  WHERE schema_name = 'temp'
              )
            THEN
              EXECUTE 'CREATE SCHEMA temp';
            END IF;
        
        END
        $$;
        ''')

        con.execute(f'''
        -- table to store props within 1km using geo gist index
        CREATE TABLE temp.{buildings_crop}
        (
            property_id integer,
            geom        geometry,
            id          serial NOT NULL
                CONSTRAINT buildings_crop_pk_{buildings_crop}
                    PRIMARY KEY
        );
        -- table to store 100 meter props out of 1km ones
        CREATE TABLE temp.{within_100m_props}
        (
            property_id integer,
            geom        geometry,
            id          serial NOT NULL
                CONSTRAINT buildings_crop_pk_{within_100m_props}
                    PRIMARY KEY
        );
        CREATE TABLE temp.{obs}
        (
            id          serial NOT NULL
                CONSTRAINT obsolescence_pk_{obs}
                    PRIMARY KEY,
            property_id integer,
            geom        geometry
        );
        ''')
        con.execute(f'''
        CREATE OR REPLACE FUNCTION temp.ST_ForceClosed_{obs}(geom geometry)
        RETURNS geometry AS
        $BODY$
        BEGIN
        IF ST_IsClosed(geom) THEN
            RETURN geom;
        ELSIF GeometryType(geom) = 'LINESTRING' THEN
            SELECT ST_AddPoint(geom, ST_StartPoint(geom)) INTO geom;
        ELSIF GeometryType(geom) ~ '(MULTI|COLLECTION)' THEN
            -- Recursively deconstruct parts
            WITH parts AS (
                SELECT temp.ST_ForceClosed_{obs}(gd.geom) AS closed_geom FROM ST_Dump(geom) AS gd
            ) -- Reconstitute parts
            SELECT ST_Collect(closed_geom)
            INTO geom
            FROM parts;
        END IF;
        IF NOT ST_IsClosed(geom) THEN
            RAISE EXCEPTION 'Could not close geometry';
        END IF;
        RETURN geom;
        END;
        $BODY$ LANGUAGE plpgsql IMMUTABLE
                            COST 42;

        CREATE OR REPLACE FUNCTION temp.ISOVIST_{buildings_crop}(IN center geometry,
                                            in prop_gis geometry,
                                           IN radius numeric DEFAULT 100,
                                           IN rays integer DEFAULT 36,
                                           IN heading integer DEFAULT -999,
                                           IN fov integer DEFAULT 360)
        RETURNS table
                (
                    p_id integer,
                    gm geometry
                )
        AS
        $$
        DECLARE
        arc     numeric;
        angle_0 numeric;
        BEGIN
        arc := fov::numeric / rays::numeric;
        IF fov = 360 THEN
            angle_0 := 0;
        ELSE
            angle_0 := heading - 0.5 * fov;
        END IF;
        RETURN QUERY
            WITH rays_all AS (
                     SELECT t.n           AS id,

                                    ST_MakeLine(
                                            center,
                                            ST_Project(
                                                    center::geography,
                                                    radius + 1,
                                                    radians(angle_0 + t.n::numeric * arc)
                                                )::geometry
                                        ) AS geom
                     FROM generate_series(0, rays) AS t(n)
                 ),
                 excluded_rays_limit AS (
                     SELECT min(id), max(id)
                     FROM rays_all
                     WHERE st_length(ST_Intersection(geom,
                                                     prop_gis)) >= 0.00001
                 ),
                 rays AS (
                     SELECT id, geom
                     FROM rays_all
                     WHERE id <
                           MOD(36 + MOD((select min from excluded_rays_limit) - 4, 36),36)
                       or id >
                           MOD(36 + MOD((select max from excluded_rays_limit) + 4, 36),36)
                 ),
                 intersections AS (
                     SELECT r.id,
                            (ST_Dump(ST_Intersection(ST_Boundary(b.geom), r.geom))).geom AS point
                     FROM rays r
                              LEFT JOIN
                          temp.{within_100m_props} b
                          ON
                              ST_Intersects(b.geom, r.geom)
                 ),
                 intersections_distances AS (
                     SELECT id,
                            point                                                         AS geom,
                            row_number() OVER (PARTITION BY id ORDER BY center <-> point) AS ranking
                     FROM intersections
                 ),
                 intersection_closest AS (
                     SELECT -1                                                      AS id,
                            CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
                     UNION ALL
                     (SELECT id,
                             geom
                      FROM intersections_distances
                      WHERE ranking = 1
                      ORDER BY ID)
                     UNION ALL
                     SELECT 999999                                                  AS id,
                            CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
                 ),
                 isovist_0 AS (
                     SELECT ST_MakePolygon(temp.ST_ForceClosed_{obs}(ST_MakeLine(geom))) AS geom
                     FROM intersection_closest
                 ),
                 isovist_buildings AS (
                     SELECT b.property_id as p_id, b.geom AS geom
                     FROM isovist_0 i,
                          temp.{within_100m_props} b
                     WHERE st_dwithin(b.geom, i.geom,
                                      0.00000001)
                 )
            SELECT b.p_id, b.geom
            FROM isovist_buildings b
        ;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
            ''')

        # store the nearby buildings in the temp building crop table
        prop_geo = raw_point.format(geo)

        con.execute(f'''
        INSERT INTO temp.{buildings_crop} (property_id, geom)
        SELECT property.id AS p_id, pg.geometry AS geom
        FROM property
                 JOIN property_gis pg ON property.id = pg.property_id
        WHERE st_dwithin(geo::geography,
                         {prop_geo}::geography, 1000)
          {COUNTY_FILTERS.get(county).surrounding_properties}
          AND property_id != {property_id}
          and property.county = '{county}'
        ''')

        # drop duplicates from temp.building_crop later we will join dropped properties
        con.execute(f'''
        delete from temp.{buildings_crop} T1
            using temp.{buildings_crop} T2
            where T1.CTID<T2.CTID
            and T1.geom = T2.geom
        ''')

        count_temp_building_crop = con.execute(f'''
        select count(*)
        from temp.{buildings_crop}
        ''').fetchone()

        if not count_temp_building_crop[0]:
            # nothing nearby....delete temp stuff....and return
            con.execute(f'''
                        -- put final results into obsolescence table
                        BEGIN;
                        insert into helper.obsolescence(property_id)
                        VALUES ({property_id});
                        
                        DROP table temp.{buildings_crop};
                        DROP table temp.{within_100m_props};
                        DROP FUNCTION if EXISTS temp.isovist_{buildings_crop}(
                            center geometry, prop_gis geometry,
                            radius numeric, rays integer, heading integer, fov integer);
                        DROP FUNCTION IF EXISTS temp.ST_ForceClosed_{obs}(geom geometry);
                        DROP table temp.{obs};
                        COMMIT;
                    ''')
            return

        CombinedGis = namedtuple('CombinedGis', ['property_id', 'county', 'geometry'])

        results = []
        results_3m = []

        pbar = tqdm(total=len(query))
        for prop in query:
            pbar.update(1)
            gis_property = CombinedGis(*prop)

            prop_gis = raw_point.format(gis_property.geometry)
            prop_id = gis_property.property_id

            con.execute(f'''
            insert into temp.{within_100m_props} (property_id, geom)
            SELECT property_id as p_id, geom
                FROM temp.{buildings_crop}
                  where st_dwithin(geom,
                                 (SELECT {prop_gis}),
                                {str(int(how_far) / 111000)})
            ''')

            query_3m = con.execute(f'''
            SELECT property_id as p_id, geom
                FROM temp.{buildings_crop}
                  where st_dwithin(geom,
                                 (SELECT {prop_gis}),
                                {str(int(3) / 111000)})
            ''').fetchall()
            for each in query_3m:
                results_3m.append((each[0], each[1]))

            equidistant_points = con.execute(f'''
                WITH polygon AS (SELECT (ST_ExteriorRing(((ST_Dump(geometry)).geom))) AS geom
                FROM property_gis WHERE property_id = {prop_id} and geometry={prop_gis}),
                     intervals AS (SELECT generate_series(0,
                (SELECT cast(st_perimeter((
                SELECT geometry 
                FROM property_gis
                WHERE property_id = {prop_id}
                and geometry = {prop_gis}
                )) * 111000 / {int(distance_between_points)} as integer))) AS steps)
                SELECT DISTINCT ST_LineInterpolatePoint(geom, steps / (SELECT count(steps)::float - 1
                FROM intervals)) AS point
                FROM polygon,
                     intervals
                GROUP BY intervals.steps, geom
                ''').fetchall()

            # eq_count = 0
            for r in equidistant_points:
                # eq_count += 1
                # print(f'computing point {eq_count}')
                point = raw_point.format(r[0])

                # if point on a property..simply pick that property  point
                container_property = con.execute(f'''
                    select * from temp.{within_100m_props}
                    WHERE st_contains(geom, {point})
                ''').fetchone()

                if container_property:
                    unformatted_gis = container_property[1]
                    results.append((container_property[0], unformatted_gis))
                    continue
                try:
                    nearby = con.execute(f'''
                    SELECT *
                    FROM temp.ISOVIST_{buildings_crop}((SELECT {point}), {prop_gis}, {how_far});
                    ''').fetchall()
                    if nearby:
                        for each in nearby:
                            results.append(each)
                except InternalError:
                    continue

        execute_values(con.connection.cursor(),
                       f"INSERT INTO temp.{obs} (property_id, geom) VALUES %s",
                       results)

        con.execute(f'''
            DELETE
            FROM temp.{obs}
            WHERE property_id NOT IN (SELECT property_id
                                      FROM temp.{obs}
                                      GROUP BY 1
                                      HAVING count(*) > {min_seen_amount}); -- property visible from at least 3
            DELETE FROM temp.{obs} T1
                USING   temp.{obs} T2
            WHERE   T1.ctid < T2.ctid  -- delete the older versions
                AND T1.property_id  = T2.property_id;
        ''')

        # insert the 3 meter props now...since min seen logic is passed
        execute_values(con.connection.cursor(),
                       f"INSERT INTO temp.{obs} (property_id, geom) VALUES %s",
                       results_3m)

        # drop the duplicates again before transferring into final obsolescence table
        con.execute(f'''
            BEGIN;

            DELETE FROM temp.{obs} T1
                USING   temp.{obs} T2
            WHERE   T1.ctid < T2.ctid  -- delete the older versions
                AND T1.property_id  = T2.property_id;

            INSERT INTO obsolescences(affected_property_id, obs_id)
            SELECT pg.property_id, {property_id}  
            FROM temp.{obs}
            JOIN property_gis pg ON temp.{obs}.geom = pg.geometry;

            insert into helper.obsolescence(property_id)
            VALUES ({property_id});

            -- put final results into obsolescence table
            DROP table temp.{buildings_crop};
            DROP table temp.{within_100m_props};
            DROP FUNCTION if EXISTS temp.isovist_{buildings_crop}(
                center geometry, prop_gis geometry,
                radius numeric, rays integer, heading integer, fov integer);
            DROP FUNCTION IF EXISTS temp.ST_ForceClosed_{obs}(geom geometry);
            DROP table temp.{obs};

            COMMIT;
        ''')

    return


# | places | degrees    | distance |
# | ------ | ---------- | -------- |
# | 0      | 1.0        | 111 km   |
# | 1      | 0.1        | 11.1 km  |
# | 2      | 0.01       | 1.11 km  |
# | 3      | 0.001      | 111 m    |
# | 4      | 0.0001     | 11.1 m   |
# | 5      | 0.00001    | 1.11 m   |
# | 6      | 0.000001   | 0.111 m  |
# | 7      | 0.0000001  | 1.11 cm  |
# | 8      | 0.00000001 | 1.11 mm  |


@bp.cli.command('compute_roads')
@click.argument('county')
def compute_roads(county):
    total = db.session.execute(f'''
        SELECT count(*)
        FROM roads
        WHERE county = '{county}'
          AND id NOT IN (SELECT DISTINCT road_id FROM road_obsolescences)
          AND id NOT IN (SELECT DISTINCT road_id from helper.scanned_roads)
         AND type IN {COUNTY_FILTERS.get(county).road_types}
--           AND type = 'railway'
        ;
    ''').fetchone()[0]

    roads = db.session.execute(f'''
        SELECT id, geometry
        FROM roads
        WHERE county = '{county}'
          AND id NOT IN (SELECT DISTINCT road_id FROM road_obsolescences)
          AND id NOT IN (SELECT DISTINCT road_id from helper.scanned_roads)
          AND type IN {COUNTY_FILTERS.get(county).road_types}    
--           AND type = 'railway'
        ;    
    ''')

    count = 1
    for road in roads:
        road_id = road[0]
        geometry = road[1]
        current_app.task_queue.enqueue(compute_road, road_id, county, geometry, count, total,
                                       job_timeout=2500)
        count += 1


@bp.cli.command('compute_single_road')
@click.argument('road_id')
def compute_single_road(road_id):
    road = Road.query.get(road_id)
    compute_road(road_id, road.county, road.geometry, 1, 1)


def compute_road(road_id, county, geometry, count, total, min_seen_amount=2, how_far=100):
    raw_point = "ST_GeomFromEWKB('\\x{}'::bytea)"

    with db.engine.connect() as conn:
        # create temp schema if not exists
        conn.execute('''
        DO $$
        BEGIN
            IF NOT EXISTS(
                SELECT schema_name
                  FROM information_schema.schemata
                  WHERE schema_name = 'temp'
              )
            THEN
              EXECUTE 'CREATE SCHEMA temp';
            END IF;
        END
        $$;
        ''')

        unique_id = uuid4().hex  # hex removes the dashes
        buildings_crop = f'roads_crop_{unique_id}'
        within_100m_props = f'near_road_props_{unique_id}'
        obs = f'road_obs_{unique_id}'

        conn.execute(f'''
            -- table to store 100 meter props out of 1km ones
            CREATE TABLE temp.{within_100m_props}
            (
                property_id integer,
                geom        geometry,
                id          serial NOT NULL
                    CONSTRAINT buildings_crop_pk_{within_100m_props}
                        PRIMARY KEY
            );
            CREATE TABLE temp.{obs}
            (
                id          serial NOT NULL
                    CONSTRAINT obsolescence_pk_{obs}
                        PRIMARY KEY,
                property_id integer,
                geom        geometry
            );
        ''')

        conn.execute(f'''
        CREATE OR REPLACE FUNCTION temp.ST_ForceClosed_{obs}(geom geometry)
        RETURNS geometry AS
        $BODY$
        BEGIN
        IF ST_IsClosed(geom) THEN
            RETURN geom;
        ELSIF GeometryType(geom) = 'LINESTRING' THEN
            SELECT ST_AddPoint(geom, ST_StartPoint(geom)) INTO geom;
        ELSIF GeometryType(geom) ~ '(MULTI|COLLECTION)' THEN
            -- Recursively deconstruct parts
            WITH parts AS (
                SELECT temp.ST_ForceClosed_{obs}(gd.geom) AS closed_geom FROM ST_Dump(geom) AS gd
            ) -- Reconstitute parts
            SELECT ST_Collect(closed_geom)
            INTO geom
            FROM parts;
        END IF;
        IF NOT ST_IsClosed(geom) THEN
            RAISE EXCEPTION 'Could not close geometry';
        END IF;
        RETURN geom;
        END;
        $BODY$ LANGUAGE plpgsql IMMUTABLE
                            COST 42;

        CREATE OR REPLACE FUNCTION temp.ISOVIST_{buildings_crop}(IN center geometry,
                                                                 IN prop_gis geometry,
                                                                 IN radius numeric DEFAULT 100,
                                                                 IN rays integer DEFAULT 36,
                                                                 IN heading integer DEFAULT -999,
                                                                 IN fov integer DEFAULT 360)
        RETURNS table
                (
                    p_id integer,
                    gm geometry
                )
        AS
        $$
        DECLARE
        arc     numeric;
        angle_0 numeric;
        BEGIN
        arc := fov::numeric / rays::numeric;
        IF fov = 360 THEN
            angle_0 := 0;
        ELSE
            angle_0 := heading - 0.5 * fov;
        END IF;
        RETURN QUERY
            WITH rays_all AS (
                     SELECT t.n           AS id,

                                    ST_MakeLine(
                                            center,
                                            ST_Project(
                                                    center::geography,
                                                    radius + 1,
                                                    radians(angle_0 + t.n::numeric * arc)
                                                )::geometry
                                        ) AS geom
                     FROM generate_series(0, rays) AS t(n)
                 ),
--                  excluded_rays_limit AS (
--                      SELECT min(id), max(id)
--                      FROM rays_all
--                      WHERE st_length(ST_Intersection(geom,
--                                                      prop_gis)) >= 0.00001
--                  ),
                 rays AS (
                     SELECT id, geom
                     FROM rays_all
                     WHERE st_length(ST_Intersection(geom,
                                                     prop_gis)) < 0.00001
                 ),
                 intersections AS (
                     SELECT r.id,
                            (ST_Dump(ST_Intersection(ST_Boundary(b.geom), r.geom))).geom AS point
                     FROM rays r
                              LEFT JOIN
                          temp.{within_100m_props} b
                          ON
                              ST_Intersects(b.geom, r.geom)
                 ),
                 intersections_distances AS (
                     SELECT id,
                            point                                                         AS geom,
                            row_number() OVER (PARTITION BY id ORDER BY center <-> point) AS ranking
                     FROM intersections
                 ),
                 intersection_closest AS (
                     SELECT -1                                                      AS id,
                            CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
                     UNION ALL
                     (SELECT id,
                             geom
                      FROM intersections_distances
                      WHERE ranking = 1
                      ORDER BY ID)
                     UNION ALL
                     SELECT 999999                                                  AS id,
                            CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
                 ),
                 isovist_0 AS (
                     SELECT ST_MakePolygon(temp.ST_ForceClosed_{obs}(ST_MakeLine(geom))) AS geom
                     FROM intersection_closest
                 ),
                 isovist_buildings AS (
                     SELECT b.property_id as p_id, b.geom AS geom
                     FROM isovist_0 i,
                          temp.{within_100m_props} b
                     WHERE st_dwithin(b.geom, i.geom,
                                      0.00000001)
                 )
            SELECT b.p_id, b.geom
            FROM isovist_buildings b
        ;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
            ''')

        results = []
        results_3m = []

        road_gis = raw_point.format(geometry)

        conn.execute(f'''
                    INSERT INTO temp.{within_100m_props} (property_id, geom)
                    SELECT property.id as p_id, pg.geometry AS geom
                    FROM property
                        JOIN property_gis pg ON property.id = pg.property_id
                          WHERE st_dwithin(pg.geometry,
                                         (SELECT {road_gis}),
                                        {str(int(how_far) / 111000)})
                          {COUNTY_FILTERS.get(county).surrounding_properties}
                          and property.county = '{county}'
        ''')

        query_3m = conn.execute(f'''
                                SELECT property.id as p_id, pg.geometry AS geom
                                FROM property
                                    JOIN property_gis pg ON property.id = pg.property_id
                                      WHERE st_dwithin(pg.geometry,
                                                     (SELECT {road_gis}),
                                                    {str(int(3) / 111000)})
                                      {COUNTY_FILTERS.get(county).surrounding_properties}
                                      and property.county = '{county}'
        ''')

        for each in query_3m:
            results_3m.append((each[0], each[1]))

        equidistant_points = db.session.execute(f'''
-- WITH intervals AS (SELECT generate_series(0,
--                                           (SELECT cast(st_length((
--                                               SELECT geometry
--                                               FROM roads
--                                               WHERE id = 526066
--                                           )) * 111000 / 5 AS INTEGER))) AS steps)
-- SELECT DISTINCT ST_LineInterpolatePoint(geometry, steps / (SELECT count(steps)::FLOAT - 1
--                                                                FROM intervals)) AS point
-- FROM roads,
--      intervals
-- WHERE id = 526066
-- GROUP BY intervals.steps, geometry;

WITH intervals AS (SELECT generate_series(0,
                                          (SELECT cast(st_length((
                                              SELECT geometry
                                              FROM roads
                                              WHERE id = {road_id}
                                          )) * 111000 / 5 AS INTEGER))) AS steps)  -- 5 is distance between points
SELECT DISTINCT ST_LineInterpolatePoint(geometry, steps / (SELECT count(steps)::FLOAT - 1
                                                               FROM intervals)) AS point
FROM roads,
     intervals
WHERE id = {road_id}
GROUP BY intervals.steps, geometry;
        ''')

        # c = 0
        for r in equidistant_points:
            # c += 1
            # print(f'computing point {c}')

            point = raw_point.format(r[0])

            # if point on a property..simply pick that property and continue with next point
            container_property = conn.execute(f'''
                select * from temp.{within_100m_props}
                WHERE st_contains(geom, {point})
            ''').fetchone()

            if container_property:
                results.append((container_property[0],
                                container_property[1]))
                continue

            try:
                nearby = conn.execute(f'''
                    SELECT *
                    FROM temp.ISOVIST_{buildings_crop}((SELECT {point}), {road_gis}, {how_far});
                ''').fetchall()
                if nearby:
                    for each in nearby:
                        results.append(each)
            except InternalError:
                continue

        execute_values(conn.connection.cursor(),
                       f"INSERT INTO temp.{obs} (property_id, geom) VALUES %s",
                       results)

        conn.execute(f'''
            DELETE
            FROM temp.{obs}
            WHERE property_id NOT IN (SELECT property_id
                                      FROM temp.{obs}
                                      GROUP BY 1
                                      HAVING count(*) > {min_seen_amount}); -- property visible from at least 3
            DELETE FROM temp.{obs} T1
                USING   temp.{obs} T2
            WHERE   T1.ctid < T2.ctid  -- delete the older versions
                AND T1.property_id  = T2.property_id;
        ''')

        # insert the 3 meter props now...since min seen logic is passed
        execute_values(conn.connection.cursor(),
                       f"INSERT INTO temp.{obs} (property_id, geom) VALUES %s",
                       results_3m)

        # drop the duplicates again before transferring into final obsolescence table
        trans = conn.begin()
        conn.execute(f'''

            DELETE FROM temp.{obs} T1
                USING   temp.{obs} T2
            WHERE   T1.ctid < T2.ctid  -- delete the older versions
                AND T1.property_id  = T2.property_id;

            INSERT INTO road_obsolescences(affected_property_id, road_id)
            SELECT property_id, {road_id}  
            FROM temp.{obs};
            --JOIN property_gis pg ON temp.{obs}.geom = pg.geometry;

            insert into helper.scanned_roads(road_id)
            VALUES ({road_id});

            DROP table temp.{within_100m_props};
            DROP FUNCTION if EXISTS temp.isovist_{buildings_crop}(
                center geometry, prop_gis geometry,
                radius numeric, rays integer, heading integer, fov integer);
            DROP FUNCTION IF EXISTS temp.ST_ForceClosed_{obs}(geom geometry);
            DROP table temp.{obs};

        ''')
        trans.commit()
    return
