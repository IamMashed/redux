# Below a set of sql queries transformed to postgresql syntax
# SQL file, come from source file used to create helper 'parcel_parid' table for the Suffolk county processing
# schema and table name are hard coded to simplify the code and parsing logic

insert_dist_cd_01_query = '''
-------------------------------------------------0100
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
                concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2),
               '00', lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(sub_sec, 2)) as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '1'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_02_query = '''
-------------------------------------------------0200
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, LEFT(block, 2), RIGHT(block, 2),
               '00', lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', LEFT(block, 2)) as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '2'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_03_query = '''
-------------------------------------------------0300
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 1), '0',
                         RIGHT(block, 2), '00', lot, sub_lot)                                          as par_id,
               concat_ws('', CAST(CAST(section AS INTEGER) as varchar(10)), '.', RIGHT(block, 1), '0') as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00')             as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot)                  as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
                 INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg)=sw.swis_cd
        WHERE sw.region = 'SUF'
          AND sw.county_name = 'Suffolk'
          AND length(sw.dist_cd) = 3
          AND LEFT(dist_cd, 1) = '3'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_04_query = '''
-------------------------------------------------0400
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, LEFT(sub_sec, 2), block, lot,
                         sub_lot)                                                                  as par_id,
               concat_ws('', CAST(CAST(section AS INTEGER) as varchar(10)), '.', LEFT(sub_sec, 2)) as sec,
               concat_ws('', CAST(CAST(LEFT(block, 2) as INTEGER) as varchar(10)), '.00')          as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot)              as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
                 INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg)=sw.swis_cd
        WHERE sw.region = 'SUF'
          AND sw.county_name = 'Suffolk'
          AND length(sw.dist_cd) = 3
          AND LEFT(dist_cd, 1) = '4'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_05_query = '''
-------------------------------------------------0500
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), RIGHT(sub_sec, 2), LEFT(block, 1),
               RIGHT(LEFT(block, 3), 2), LEFT(concat_ws('', RIGHT(block, 1), lot), 2),
               RIGHT(concat_ws('', RIGHT(block, 1), lot), 2), sub_lot, suffix) as par_id,
               concat_ws('', CAST(CAST (concat_ws('', RIGHT(sub_sec, 2), LEFT(block, 1)) AS INTEGER) as varchar(10)),
               '.', RIGHT(LEFT(block, 3), 2)) as sec,
               concat_ws('', CAST(CAST(LEFT(concat_ws('', RIGHT(block, 1), lot), 2) as INTEGER) as varchar(10)), '.',
               RIGHT(concat_ws('', RIGHT(block, 1), lot), 2)) as block,
               concat_ws('', CAST(CAST(sub_lot as INTEGER) as varchar(10)), '.', suffix) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '5'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_06_query = '''
-------------------------------------------------0600
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2),
               '00', lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(sub_sec, 2)) as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '6'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_07_query = '''
-------------------------------------------------0700
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section,
               RIGHT(concat_ws('', '00', sub_sec), 2),
                   CASE
                       WHEN LEFT(block, 2) = '00'
                           THEN concat_ws('', RIGHT(concat_ws('', '00', block), 2), '00')
                       ELSE concat_ws('', RIGHT(block, 2), LEFT(block, 2))
                       END, lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.',
               RIGHT(concat_ws('', '00', sub_sec), 2)) as sec,
               (CASE
                   WHEN LEFT(block, 2) = '00'
                       THEN concat_ws('', RIGHT(concat_ws('', '00', block), 2), '.00')
                   ELSE concat_ws('', RIGHT(block, 2), '.', LEFT(block, 2))
                   END) as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '7'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_08_query = '''
-------------------------------------------------0800
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2),
               '00', lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(sub_sec, 2)) as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '8'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_09_query = '''
-------------------------------------------------0900
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
    SELECT
           p.muni_code,
           p.parcel_id,
           concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2),
           '00', lot, sub_lot) as par_id,
           concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(sub_sec, 2)) as sec,
           concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
           concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
           sw.dist_cd,
           print_key
    FROM data_source.suffolk_parcel p
    INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
    WHERE
          sw.region = 'SUF'
    AND
          sw.county_name = 'Suffolk'
    AND
          length(sw.dist_cd) = 3
    AND
          LEFT(dist_cd, 1) = '9'
    ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

insert_dist_cd_10_query = '''
-------------------------------------------------1000
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2),
               '00', lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(sub_sec, 2)) as sec,
               concat_ws('', CAST(CAST(RIGHT(block, 2) as INTEGER) as varchar(10)), '.00') as block,
               concat_ws('', CAST(CAST(lot as INTEGER) as varchar(10)), '.', sub_lot) as lot,
               sw.dist_cd,
               print_key
        FROM data_source.suffolk_parcel p
        INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE
              sw.region = 'SUF'
        AND
              sw.county_name = 'Suffolk'
        AND
              length(sw.dist_cd) = 3
        AND
              LEFT(dist_cd, 1) = '10'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;
'''

# set of insert queries
parcel_parid_insert_queries = [
    insert_dist_cd_01_query, insert_dist_cd_02_query, insert_dist_cd_03_query, insert_dist_cd_04_query,
    insert_dist_cd_05_query, insert_dist_cd_06_query, insert_dist_cd_07_query, insert_dist_cd_08_query,
    insert_dist_cd_09_query, insert_dist_cd_10_query
]

update_parcel_fields_query = '''
-- update suffolk parcel information
UPDATE public.property
SET (district, section, block, lot, number, street, town, state, zip,
     coordinate_x, coordinate_y, undefined_field, print_key, address_line_1, address_line_2) =
    (
     spp.dist_cd, spp.sec, spp.block, spp.lot, sp.loc_st_nbr, sp.loc_st_name, sw.town_nm, sp.state, sp.loc_zip::int,
    sp.grid_east::double precision, sp.grid_north::double precision, spp.muni_code, spp.print_key, sp.address_line_1,
     sp.address_line_2
    )
from data_source.suffolk_parcel sp
    inner join data_source.suffolk_parcel_parid spp on (spp.parcel_id=sp.parcel_id and spp.muni_code=sp.muni_code)
    inner join data_source.suffolk_swis sw on concat_ws('', sp.swis_co, sp.swis_muni, sp.swis_vlg) = sw.swis_cd
WHERE public.property.apn = spp.par_id
and public.property.county = 'suffolk';

-- additionally update full address
update public.property
set address = concat_ws(' ', address_line_1, address_line_2, town, state, zip)
where county='suffolk';
'''

update_res_bldg_inventories_query = '''
-- update suffolk property inventory from res_bldg.txt
UPDATE public.property
SET (
        property_style,  gla_sqft, story_height, age, basement_type, full_baths,
        half_baths, rooms, bedrooms, kitchens, fireplaces, heat_type, condition, effective_age
    ) =
    (
        rb.property_style,
        rb.sqft_living_area::double precision, rb.nbr_stories::double precision, rb.yr_blt::double precision,
        rb.bsmnt_type::double precision, rb.nbr_full_baths::double precision,
        rb.nbr_half_baths::double precision, rb.nbr_rooms::double precision, rb.nbr_bed::double precision,
        rb.nbr_kitchens::double precision, rb.nbr_fireplaces::double precision, rb.heat_type, rb.interior_cond,
        rb.yr_remodeled::double precision
    )
from data_source.suffolk_parcel sp
    inner join data_source.suffolk_parcel_parid spp on (spp.parcel_id=sp.parcel_id and spp.muni_code=sp.muni_code)
    inner join data_source.suffolk_res_bldg rb on (rb.muni_code = sp.muni_code and rb.parcel_id = sp.parcel_id)
    inner join public.property p on p.apn = spp.par_id
WHERE property.apn = spp.par_id
AND property.county = 'suffolk';
'''
