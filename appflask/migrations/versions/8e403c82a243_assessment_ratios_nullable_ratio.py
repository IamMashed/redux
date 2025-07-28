"""assessment ratios nullable ratio

Revision ID: 8e403c82a243
Revises: f88d20bc7dc0
Create Date: 2019-12-19 18:54:03.827098

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e403c82a243'
down_revision = 'f88d20bc7dc0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('assessment_ratio', 'ratio',
                    existing_type=postgresql.DOUBLE_PRECISION(precision=53),
                    nullable=True)
    op.execute('''
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (2, 'suffolk', 100, 'Babylon', 2018, 1.07, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (3, 'suffolk', 200, 'Brookhaven', 2018, 0.86, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (4, 'suffolk', 300, 'East Hampton', 2018, 0.58, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (5, 'suffolk', 400, 'Huntington', 2018, 0.69, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (6, 'suffolk', 500, 'Islip', 2018, 11.35, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (7, 'suffolk', 600, 'Riverhead', 2018, 13.52, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (8, 'suffolk', 800, 'Smithtown', 2018, 1.23, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (9, 'suffolk', 900, 'Southampton', 2018, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (10, 'suffolk', 1000, 'Southold', 2018, 0.94, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (11, 'suffolk', 100, 'Babylon', 2017, 1.12, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (12, 'suffolk', 200, 'Brookhaven', 2017, 0.9, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (13, 'suffolk', 300, 'East Hampton', 2017, 0.57, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (14, 'suffolk', 400, 'Huntington', 2017, 0.71, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (15, 'suffolk', 500, 'Islip', 2017, 12.12, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (16, 'suffolk', 600, 'Riverhead', 2017, 13.87, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (17, 'suffolk', 800, 'Smithtown', 2017, 1.31, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (18, 'suffolk', 900, 'Southampton', 2017, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (19, 'suffolk', 1000, 'Southold', 2017, 1.01, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (20, 'suffolk', 100, 'Babylon', 2016, 1.18, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (21, 'suffolk', 200, 'Brookhaven', 2016, 0.91, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (22, 'suffolk', 300, 'East Hampton', 2016, 0.59, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (23, 'suffolk', 400, 'Huntington', 2016, 0.73, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (24, 'suffolk', 500, 'Islip', 2016, 12.7, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (25, 'suffolk', 600, 'Riverhead', 2016, 14.66, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (26, 'suffolk', 800, 'Smithtown', 2016, 1.32, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (27, 'suffolk', 900, 'Southampton', 2016, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (28, 'suffolk', 1000, 'Southold', 2016, 1.08, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (29, 'suffolk', 100, 'Babylon', 2015, 1.19, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (30, 'suffolk', 200, 'Brookhaven', 2015, 0.95, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (31, 'suffolk', 300, 'East Hampton', 2015, 0.64, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (32, 'suffolk', 400, 'Huntington', 2015, 0.73, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (33, 'suffolk', 500, 'Islip', 2015, 12.7, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (34, 'suffolk', 600, 'Riverhead', 2015, 14.58, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (35, 'suffolk', 800, 'Smithtown', 2015, 1.3, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (36, 'suffolk', 900, 'Southampton', 2015, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (37, 'suffolk', 1000, 'Southold', 2015, 1.1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (38, 'suffolk', 100, 'Babylon', 2014, 1.25, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (39, 'suffolk', 200, 'Brookhaven', 2014, 0.95, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (40, 'suffolk', 300, 'East Hampton', 2014, 0.73, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (41, 'suffolk', 400, 'Huntington', 2014, 0.77, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (42, 'suffolk', 500, 'Islip', 2014, 13.2, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (43, 'suffolk', 600, 'Riverhead', 2014, 15.4, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (44, 'suffolk', 800, 'Smithtown', 2014, 1.37, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (45, 'suffolk', 900, 'Southampton', 2014, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (46, 'suffolk', 1000, 'Southold', 2014, 1.17, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (47, 'suffolk', 100, 'Babylon', 2013, 1.23, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (48, 'suffolk', 200, 'Brookhaven', 2013, 0.95, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (49, 'suffolk', 300, 'East Hampton', 2013, 0.73, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (50, 'suffolk', 400, 'Huntington', 2013, 0.79, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (51, 'suffolk', 500, 'Islip', 2013, 13.2, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (52, 'suffolk', 600, 'Riverhead', 2013, 15.98, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (53, 'suffolk', 800, 'Smithtown', 2013, 1.37, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (54, 'suffolk', 900, 'Southampton', 2013, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (55, 'suffolk', 1000, 'Southold', 2013, 1.18, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (56, 'suffolk', 100, 'Babylon', 2012, 1.13, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (57, 'suffolk', 200, 'Brookhaven', 2012, 0.9, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (58, 'suffolk', 300, 'East Hampton', 2012, 0.76, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (59, 'suffolk', 400, 'Huntington', 2012, 0.77, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (60, 'suffolk', 500, 'Islip', 2012, 12.38, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (61, 'suffolk', 600, 'Riverhead', 2012, 14.02, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (62, 'suffolk', 800, 'Smithtown', 2012, 1.28, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (63, 'suffolk', 900, 'Southampton', 2012, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (64, 'suffolk', 1000, 'Southold', 2012, 1.11, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (72, 'suffolk', 900, 'Southampton', 2019, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (73, 'suffolk', 1000, 'Southold', 2019, 0.93, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (68, 'suffolk', 400, 'Huntington', 2019, 0.65, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (69, 'suffolk', 500, 'Islip', 2019, 10.77, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (70, 'suffolk', 600, 'Riverhead', 2019, 12.35, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (71, 'suffolk', 800, 'Smithtown', 2019, 1.16, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (65, 'suffolk', 100, 'Babylon', 2019, 0.97, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (66, 'suffolk', 200, 'Brookhaven', 2019, 0.79, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (67, 'suffolk', 300, 'East Hampton', 2019, 0.56, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (77, 'suffolk', 500, 'Islip', 2011, 11.37, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (79, 'suffolk', 800, 'Smithtown', 2011, 1.23, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (80, 'suffolk', 100, 'Babylon', 2011, 1.05, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (82, 'suffolk', 300, 'East Hampton', 2011, 0.74, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (81, 'suffolk', 200, 'Brookhaven', 2011, 0.87, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (75, 'suffolk', 1000, 'Southold', 2011, 1.07, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (74, 'suffolk', 900, 'Southampton', 2011, 1, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (76, 'suffolk', 400, 'Huntington', 2011, 0.75, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (78, 'suffolk', 600, 'Riverhead', 2011, 14.23, null);
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (83, 'nassau', 282223, 'Mineola
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (84, 'nassau', 282005, 'East Rockaway
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (85, 'nassau', 282011, 'Garden City
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (86, 'nassau', 282029, 'Rockville Centre
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (87, 'nassau', 282021, 'Island Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (88, 'nassau', 282209, 'Great Neck
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (89, 'nassau', 282249, 'Saddle Rock
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (90, 'nassau', 282027, 'Malverne
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (91, 'nassau', 282007, 'Floral Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (92, 'nassau', 282239, 'Port Washington North
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (93, 'nassau', 282035, 'Valley Stream
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (94, 'nassau', 282257, 'Williston Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (95, 'nassau', 282423, 'Sea Cliff
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (96, 'nassau', 282203, 'East Hills
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (97, 'nassau', 282255, 'Westbury
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (98, 'nassau', 282025, 'Lynbrook
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (99, 'nassau', 282215, 'Kensington
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (100, 'nassau', 282013, 'Hempstead
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (101, 'nassau', 282231, 'Old Westbury
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (102, 'nassau', 282247, 'Russell Gardens
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (103, 'nassau', 282205, 'East Williston
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (104, 'nassau', 282217, 'Kings Point
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (105, 'nassau', 282227, 'New Hyde Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (106, 'nassau', 282041, 'New Hyde Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (107, 'nassau', 282241, 'Roslyn
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (108, 'nassau', 282211, 'Great Neck Estates
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (109, 'nassau', 282023, 'Lawrence
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (110, 'nassau', 282219, 'Lake Success
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (111, 'nassau', 282259, 'Floral Park
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (112, 'nassau', 282009, 'Freeport
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (113, 'nassau', 282213, 'Great Neck Plaza
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (114, 'nassau', 282253, 'Thomaston
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (115, 'nassau', 282415, 'Old Brookville
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (116, 'nassau', 282429, 'Muttontown
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (117, 'nassau', 282409, 'Farmingdale
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (118, 'nassau', 282243, 'Roslyn Estates
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (119, 'nassau', 282251, 'Sands Point
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (120, 'nassau', 282411, 'Lattingtown
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (121, 'nassau', 282403, 'Brookville
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (122, 'nassau', 282431, 'Old Westbury
', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (123, 'nassau', 282031, 'South Floral Park', 2021, 0.001, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (124, 'nassau', 282223, 'Mineola
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (125, 'nassau', 282005, 'East Rockaway
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (126, 'nassau', 282011, 'Garden City
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (127, 'nassau', 282029, 'Rockville Centre
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (128, 'nassau', 282021, 'Island Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (129, 'nassau', 282209, 'Great Neck
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (130, 'nassau', 282249, 'Saddle Rock
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (131, 'nassau', 282027, 'Malverne
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (132, 'nassau', 282007, 'Floral Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (133, 'nassau', 282239, 'Port Washington North
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (134, 'nassau', 282035, 'Valley Stream
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (135, 'nassau', 282257, 'Williston Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (136, 'nassau', 282423, 'Sea Cliff
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (137, 'nassau', 282203, 'East Hills
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (138, 'nassau', 282255, 'Westbury
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (139, 'nassau', 282025, 'Lynbrook
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (140, 'nassau', 282215, 'Kensington
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (141, 'nassau', 282013, 'Hempstead
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (142, 'nassau', 282231, 'Old Westbury
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (143, 'nassau', 282247, 'Russell Gardens
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (144, 'nassau', 282205, 'East Williston
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (145, 'nassau', 282217, 'Kings Point
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (146, 'nassau', 282227, 'New Hyde Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (147, 'nassau', 282041, 'New Hyde Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (148, 'nassau', 282241, 'Roslyn
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (149, 'nassau', 282211, 'Great Neck Estates
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (150, 'nassau', 282023, 'Lawrence
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (151, 'nassau', 282219, 'Lake Success
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (152, 'nassau', 282259, 'Floral Park
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (153, 'nassau', 282009, 'Freeport
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (154, 'nassau', 282213, 'Great Neck Plaza
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (155, 'nassau', 282253, 'Thomaston
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (156, 'nassau', 282415, 'Old Brookville
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (157, 'nassau', 282429, 'Muttontown
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (158, 'nassau', 282409, 'Farmingdale
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (159, 'nassau', 282243, 'Roslyn Estates
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (160, 'nassau', 282251, 'Sands Point
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (161, 'nassau', 282411, 'Lattingtown
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (162, 'nassau', 282403, 'Brookville
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (163, 'nassau', 282431, 'Old Westbury
', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (164, 'nassau', 282031, 'South Floral Park', 2020, 0.0014, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (165, 'nassau', 282223, 'Mineola
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (166, 'nassau', 282005, 'East Rockaway
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (167, 'nassau', 282011, 'Garden City
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (168, 'nassau', 282029, 'Rockville Centre
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (169, 'nassau', 282021, 'Island Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (170, 'nassau', 282209, 'Great Neck
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (171, 'nassau', 282249, 'Saddle Rock
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (172, 'nassau', 282027, 'Malverne
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (173, 'nassau', 282007, 'Floral Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (174, 'nassau', 282239, 'Port Washington North
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (175, 'nassau', 282035, 'Valley Stream
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (176, 'nassau', 282257, 'Williston Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (177, 'nassau', 282423, 'Sea Cliff
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (178, 'nassau', 282203, 'East Hills
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (179, 'nassau', 282255, 'Westbury
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (180, 'nassau', 282025, 'Lynbrook
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (181, 'nassau', 282215, 'Kensington
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (182, 'nassau', 282013, 'Hempstead
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (183, 'nassau', 282231, 'Old Westbury
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (184, 'nassau', 282247, 'Russell Gardens
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (185, 'nassau', 282205, 'East Williston
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (186, 'nassau', 282217, 'Kings Point
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (187, 'nassau', 282227, 'New Hyde Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (188, 'nassau', 282041, 'New Hyde Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (189, 'nassau', 282241, 'Roslyn
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (190, 'nassau', 282211, 'Great Neck Estates
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (191, 'nassau', 282023, 'Lawrence
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (192, 'nassau', 282219, 'Lake Success
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (193, 'nassau', 282259, 'Floral Park
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (194, 'nassau', 282009, 'Freeport
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (195, 'nassau', 282213, 'Great Neck Plaza
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (196, 'nassau', 282253, 'Thomaston
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (197, 'nassau', 282415, 'Old Brookville
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (198, 'nassau', 282429, 'Muttontown
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (199, 'nassau', 282409, 'Farmingdale
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (200, 'nassau', 282243, 'Roslyn Estates
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (201, 'nassau', 282251, 'Sands Point
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (202, 'nassau', 282411, 'Lattingtown
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (203, 'nassau', 282403, 'Brookville
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (204, 'nassau', 282431, 'Old Westbury
', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (205, 'nassau', 282031, 'South Floral Park', 2019, 0.0015, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (206, 'nassau', 282223, 'Mineola
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (207, 'nassau', 282005, 'East Rockaway
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (208, 'nassau', 282011, 'Garden City
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (209, 'nassau', 282029, 'Rockville Centre
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (210, 'nassau', 282021, 'Island Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (211, 'nassau', 282209, 'Great Neck
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (212, 'nassau', 282249, 'Saddle Rock
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (213, 'nassau', 282027, 'Malverne
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (214, 'nassau', 282007, 'Floral Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (215, 'nassau', 282239, 'Port Washington North
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (216, 'nassau', 282035, 'Valley Stream
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (217, 'nassau', 282257, 'Williston Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (218, 'nassau', 282423, 'Sea Cliff
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (219, 'nassau', 282203, 'East Hills
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (220, 'nassau', 282255, 'Westbury
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (221, 'nassau', 282025, 'Lynbrook
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (222, 'nassau', 282215, 'Kensington
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (223, 'nassau', 282013, 'Hempstead
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (224, 'nassau', 282231, 'Old Westbury
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (225, 'nassau', 282247, 'Russell Gardens
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (226, 'nassau', 282205, 'East Williston
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (227, 'nassau', 282217, 'Kings Point
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (228, 'nassau', 282227, 'New Hyde Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (229, 'nassau', 282041, 'New Hyde Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (230, 'nassau', 282241, 'Roslyn
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (231, 'nassau', 282211, 'Great Neck Estates
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (232, 'nassau', 282023, 'Lawrence
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (233, 'nassau', 282219, 'Lake Success
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (234, 'nassau', 282259, 'Floral Park
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (235, 'nassau', 282009, 'Freeport
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (236, 'nassau', 282213, 'Great Neck Plaza
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (237, 'nassau', 282253, 'Thomaston
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (238, 'nassau', 282415, 'Old Brookville
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (239, 'nassau', 282429, 'Muttontown
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (240, 'nassau', 282409, 'Farmingdale
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (241, 'nassau', 282243, 'Roslyn Estates
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (242, 'nassau', 282251, 'Sands Point
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (243, 'nassau', 282411, 'Lattingtown
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (244, 'nassau', 282403, 'Brookville
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (245, 'nassau', 282431, 'Old Westbury
', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (246, 'nassau', 282031, 'South Floral Park', 2018, 0.0016, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (247, 'nassau', 282223, 'Mineola
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (248, 'nassau', 282005, 'East Rockaway
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (249, 'nassau', 282011, 'Garden City
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (250, 'nassau', 282029, 'Rockville Centre
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (251, 'nassau', 282021, 'Island Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (252, 'nassau', 282209, 'Great Neck
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (253, 'nassau', 282249, 'Saddle Rock
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (254, 'nassau', 282027, 'Malverne
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (255, 'nassau', 282007, 'Floral Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (256, 'nassau', 282239, 'Port Washington North
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (257, 'nassau', 282035, 'Valley Stream
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (258, 'nassau', 282257, 'Williston Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (259, 'nassau', 282423, 'Sea Cliff
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (260, 'nassau', 282203, 'East Hills
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (261, 'nassau', 282255, 'Westbury
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (262, 'nassau', 282025, 'Lynbrook
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (263, 'nassau', 282215, 'Kensington
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (264, 'nassau', 282013, 'Hempstead
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (265, 'nassau', 282231, 'Old Westbury
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (266, 'nassau', 282247, 'Russell Gardens
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (267, 'nassau', 282205, 'East Williston
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (268, 'nassau', 282217, 'Kings Point
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (269, 'nassau', 282227, 'New Hyde Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (270, 'nassau', 282041, 'New Hyde Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (271, 'nassau', 282241, 'Roslyn
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (272, 'nassau', 282211, 'Great Neck Estates
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (273, 'nassau', 282023, 'Lawrence
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (274, 'nassau', 282219, 'Lake Success
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (275, 'nassau', 282259, 'Floral Park
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (276, 'nassau', 282009, 'Freeport
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (277, 'nassau', 282213, 'Great Neck Plaza
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (278, 'nassau', 282253, 'Thomaston
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (279, 'nassau', 282415, 'Old Brookville
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (280, 'nassau', 282429, 'Muttontown
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (281, 'nassau', 282409, 'Farmingdale
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (282, 'nassau', 282243, 'Roslyn Estates
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (283, 'nassau', 282251, 'Sands Point
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (284, 'nassau', 282411, 'Lattingtown
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (285, 'nassau', 282403, 'Brookville
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (286, 'nassau', 282431, 'Old Westbury
', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (287, 'nassau', 282031, 'South Floral Park', 2017, 0.0017, 'Nassau First Level ARC');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (288, 'nassau', 282223, 'Mineola
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (289, 'nassau', 282005, 'East Rockaway
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (290, 'nassau', 282011, 'Garden City
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (291, 'nassau', 282029, 'Rockville Centre
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (292, 'nassau', 282021, 'Island Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (293, 'nassau', 282209, 'Great Neck
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (294, 'nassau', 282249, 'Saddle Rock
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (295, 'nassau', 282027, 'Malverne
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (296, 'nassau', 282007, 'Floral Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (297, 'nassau', 282239, 'Port Washington North
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (298, 'nassau', 282035, 'Valley Stream
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (299, 'nassau', 282257, 'Williston Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (300, 'nassau', 282423, 'Sea Cliff
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (301, 'nassau', 282203, 'East Hills
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (302, 'nassau', 282255, 'Westbury
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (303, 'nassau', 282025, 'Lynbrook
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (304, 'nassau', 282215, 'Kensington
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (305, 'nassau', 282013, 'Hempstead
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (306, 'nassau', 282231, 'Old Westbury
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (307, 'nassau', 282247, 'Russell Gardens
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (308, 'nassau', 282205, 'East Williston
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (309, 'nassau', 282217, 'Kings Point
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (310, 'nassau', 282227, 'New Hyde Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (311, 'nassau', 282041, 'New Hyde Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (312, 'nassau', 282241, 'Roslyn
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (313, 'nassau', 282211, 'Great Neck Estates
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (314, 'nassau', 282023, 'Lawrence
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (315, 'nassau', 282219, 'Lake Success
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (316, 'nassau', 282259, 'Floral Park
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (317, 'nassau', 282009, 'Freeport
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (318, 'nassau', 282213, 'Great Neck Plaza
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (319, 'nassau', 282253, 'Thomaston
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (320, 'nassau', 282415, 'Old Brookville
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (321, 'nassau', 282429, 'Muttontown
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (322, 'nassau', 282409, 'Farmingdale
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (323, 'nassau', 282243, 'Roslyn Estates
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (324, 'nassau', 282251, 'Sands Point
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (325, 'nassau', 282411, 'Lattingtown
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (326, 'nassau', 282403, 'Brookville
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (327, 'nassau', 282431, 'Old Westbury
', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (328, 'nassau', 282031, 'South Floral Park', 2017, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (329, 'nassau', 282223, 'Mineola
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (330, 'nassau', 282005, 'East Rockaway
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (331, 'nassau', 282011, 'Garden City
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (332, 'nassau', 282029, 'Rockville Centre
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (333, 'nassau', 282021, 'Island Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (334, 'nassau', 282209, 'Great Neck
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (335, 'nassau', 282249, 'Saddle Rock
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (336, 'nassau', 282027, 'Malverne
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (337, 'nassau', 282007, 'Floral Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (338, 'nassau', 282239, 'Port Washington North
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (339, 'nassau', 282035, 'Valley Stream
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (340, 'nassau', 282257, 'Williston Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (341, 'nassau', 282423, 'Sea Cliff
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (342, 'nassau', 282203, 'East Hills
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (343, 'nassau', 282255, 'Westbury
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (344, 'nassau', 282025, 'Lynbrook
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (345, 'nassau', 282215, 'Kensington
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (346, 'nassau', 282013, 'Hempstead
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (347, 'nassau', 282231, 'Old Westbury
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (348, 'nassau', 282247, 'Russell Gardens
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (349, 'nassau', 282205, 'East Williston
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (350, 'nassau', 282217, 'Kings Point
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (351, 'nassau', 282227, 'New Hyde Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (352, 'nassau', 282041, 'New Hyde Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (353, 'nassau', 282241, 'Roslyn
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (354, 'nassau', 282211, 'Great Neck Estates
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (355, 'nassau', 282023, 'Lawrence
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (356, 'nassau', 282219, 'Lake Success
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (357, 'nassau', 282259, 'Floral Park
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (358, 'nassau', 282009, 'Freeport
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (359, 'nassau', 282213, 'Great Neck Plaza
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (360, 'nassau', 282253, 'Thomaston
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (361, 'nassau', 282415, 'Old Brookville
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (362, 'nassau', 282429, 'Muttontown
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (363, 'nassau', 282409, 'Farmingdale
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (364, 'nassau', 282243, 'Roslyn Estates
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (365, 'nassau', 282251, 'Sands Point
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (366, 'nassau', 282411, 'Lattingtown
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (367, 'nassau', 282403, 'Brookville
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (368, 'nassau', 282431, 'Old Westbury
', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (369, 'nassau', 282031, 'South Floral Park', 2018, 0.0018, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (370, 'nassau', 282223, 'Mineola
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (371, 'nassau', 282005, 'East Rockaway
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (372, 'nassau', 282011, 'Garden City
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (373, 'nassau', 282029, 'Rockville Centre
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (374, 'nassau', 282021, 'Island Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (375, 'nassau', 282209, 'Great Neck
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (376, 'nassau', 282249, 'Saddle Rock
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (377, 'nassau', 282027, 'Malverne
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (378, 'nassau', 282007, 'Floral Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (379, 'nassau', 282239, 'Port Washington North
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (380, 'nassau', 282035, 'Valley Stream
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (381, 'nassau', 282257, 'Williston Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (382, 'nassau', 282423, 'Sea Cliff
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (383, 'nassau', 282203, 'East Hills
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (384, 'nassau', 282255, 'Westbury
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (385, 'nassau', 282025, 'Lynbrook
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (386, 'nassau', 282215, 'Kensington
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (387, 'nassau', 282013, 'Hempstead
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (388, 'nassau', 282231, 'Old Westbury
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (389, 'nassau', 282247, 'Russell Gardens
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (390, 'nassau', 282205, 'East Williston
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (391, 'nassau', 282217, 'Kings Point
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (392, 'nassau', 282227, 'New Hyde Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (393, 'nassau', 282041, 'New Hyde Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (394, 'nassau', 282241, 'Roslyn
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (395, 'nassau', 282211, 'Great Neck Estates
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (396, 'nassau', 282023, 'Lawrence
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (397, 'nassau', 282219, 'Lake Success
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (398, 'nassau', 282259, 'Floral Park
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (399, 'nassau', 282009, 'Freeport
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (400, 'nassau', 282213, 'Great Neck Plaza
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (401, 'nassau', 282253, 'Thomaston
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (402, 'nassau', 282415, 'Old Brookville
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (403, 'nassau', 282429, 'Muttontown
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (404, 'nassau', 282409, 'Farmingdale
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (405, 'nassau', 282243, 'Roslyn Estates
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (406, 'nassau', 282251, 'Sands Point
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (407, 'nassau', 282411, 'Lattingtown
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (408, 'nassau', 282403, 'Brookville
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (409, 'nassau', 282431, 'Old Westbury
', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (410, 'nassau', 282031, 'South Floral Park', 2019, 0.0017, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (411, 'nassau', 282223, 'Mineola
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (412, 'nassau', 282005, 'East Rockaway
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (413, 'nassau', 282011, 'Garden City
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (414, 'nassau', 282029, 'Rockville Centre
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (415, 'nassau', 282021, 'Island Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (416, 'nassau', 282209, 'Great Neck
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (417, 'nassau', 282249, 'Saddle Rock
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (418, 'nassau', 282027, 'Malverne
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (419, 'nassau', 282007, 'Floral Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (420, 'nassau', 282239, 'Port Washington North
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (421, 'nassau', 282035, 'Valley Stream
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (422, 'nassau', 282257, 'Williston Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (423, 'nassau', 282423, 'Sea Cliff
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (424, 'nassau', 282203, 'East Hills
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (425, 'nassau', 282255, 'Westbury
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (426, 'nassau', 282025, 'Lynbrook
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (427, 'nassau', 282215, 'Kensington
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (428, 'nassau', 282013, 'Hempstead
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (429, 'nassau', 282231, 'Old Westbury
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (430, 'nassau', 282247, 'Russell Gardens
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (431, 'nassau', 282205, 'East Williston
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (432, 'nassau', 282217, 'Kings Point
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (433, 'nassau', 282227, 'New Hyde Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (434, 'nassau', 282041, 'New Hyde Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (435, 'nassau', 282241, 'Roslyn
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (436, 'nassau', 282211, 'Great Neck Estates
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (437, 'nassau', 282023, 'Lawrence
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (438, 'nassau', 282219, 'Lake Success
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (439, 'nassau', 282259, 'Floral Park
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (440, 'nassau', 282009, 'Freeport
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (441, 'nassau', 282213, 'Great Neck Plaza
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (442, 'nassau', 282253, 'Thomaston
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (443, 'nassau', 282415, 'Old Brookville
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (444, 'nassau', 282429, 'Muttontown
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (445, 'nassau', 282409, 'Farmingdale
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (446, 'nassau', 282243, 'Roslyn Estates
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (447, 'nassau', 282251, 'Sands Point
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (448, 'nassau', 282411, 'Lattingtown
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (449, 'nassau', 282403, 'Brookville
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (450, 'nassau', 282431, 'Old Westbury
', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (451, 'nassau', 282031, 'South Floral Park', 2020, 0.0015, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (453, 'nassau', 282223, 'Mineola
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (454, 'nassau', 282005, 'East Rockaway
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (455, 'nassau', 282011, 'Garden City
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (456, 'nassau', 282029, 'Rockville Centre
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (457, 'nassau', 282021, 'Island Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (458, 'nassau', 282209, 'Great Neck
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (459, 'nassau', 282249, 'Saddle Rock
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (460, 'nassau', 282027, 'Malverne
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (461, 'nassau', 282007, 'Floral Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (462, 'nassau', 282239, 'Port Washington North
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (463, 'nassau', 282035, 'Valley Stream
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (464, 'nassau', 282257, 'Williston Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (465, 'nassau', 282423, 'Sea Cliff
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (466, 'nassau', 282203, 'East Hills
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (467, 'nassau', 282255, 'Westbury
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (468, 'nassau', 282025, 'Lynbrook
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (469, 'nassau', 282215, 'Kensington
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (470, 'nassau', 282013, 'Hempstead
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (471, 'nassau', 282231, 'Old Westbury
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (472, 'nassau', 282247, 'Russell Gardens
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (473, 'nassau', 282205, 'East Williston
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (474, 'nassau', 282217, 'Kings Point
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (475, 'nassau', 282227, 'New Hyde Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (476, 'nassau', 282041, 'New Hyde Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (477, 'nassau', 282241, 'Roslyn
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (478, 'nassau', 282211, 'Great Neck Estates
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (479, 'nassau', 282023, 'Lawrence
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (480, 'nassau', 282219, 'Lake Success
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (481, 'nassau', 282259, 'Floral Park
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (482, 'nassau', 282009, 'Freeport
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (483, 'nassau', 282213, 'Great Neck Plaza
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (484, 'nassau', 282253, 'Thomaston
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (485, 'nassau', 282415, 'Old Brookville
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (486, 'nassau', 282429, 'Muttontown
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (487, 'nassau', 282409, 'Farmingdale
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (488, 'nassau', 282243, 'Roslyn Estates
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (489, 'nassau', 282251, 'Sands Point
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (490, 'nassau', 282411, 'Lattingtown
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (491, 'nassau', 282403, 'Brookville
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (492, 'nassau', 282431, 'Old Westbury
', 2021, null, 'Nassau Second Level SCAR');
INSERT INTO public.assessment_ratio (id, county, town_code, town_name, year, ratio, level) VALUES (493, 'nassau', 282031, 'South Floral Park', 2021, null, 'Nassau Second Level SCAR');    
''')
    # ### end Alembic commands ###


def downgrade():
    op.execute('''truncate assessment_ratio''')
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('assessment_ratio', 'ratio',
                    existing_type=postgresql.DOUBLE_PRECISION(precision=53),
                    nullable=False)
    # ### end Alembic commands ###
