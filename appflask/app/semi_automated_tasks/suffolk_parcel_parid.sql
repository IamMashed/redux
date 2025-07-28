
CREATE TABLE suffolk_parcel_parid (
    muni_code   varchar,
    parcel_id   varchar,
    par_id      varchar,
    sec         varchar,
    block       varchar,
    lot         varchar,
    dist_cd     varchar,
    print_key   varchar
);

-------------------------------------------------0100
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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
    );

-------------------------------------------------0200
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, LEFT(block, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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
                 INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE sw.region = 'SUF'
          AND sw.county_name = 'Suffolk'
          AND length(sw.dist_cd) = 3
          AND LEFT(dist_cd, 1) = '3'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;


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
                 INNER JOIN data_source.suffolk_swis sw on concat_ws('', p.swis_co, p.swis_muni, p.swis_vlg) = sw.swis_cd
        WHERE sw.region = 'SUF'
          AND sw.county_name = 'Suffolk'
          AND length(sw.dist_cd) = 3
          AND LEFT(dist_cd, 1) = '4'
        ORDER BY p.muni_code, p.parcel_id
    )
ON CONFLICT DO NOTHING;

-------------------------------------------------0500
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), RIGHT(sub_sec, 2), LEFT(block, 1), RIGHT(LEFT(block, 3), 2), LEFT(concat_ws('', RIGHT(block, 1), lot), 2), RIGHT(concat_ws('', RIGHT(block, 1), lot), 2), sub_lot, suffix) as par_id,
               concat_ws('', CAST(CAST (concat_ws('', RIGHT(sub_sec, 2), LEFT(block, 1)) AS INTEGER) as varchar(10)), '.', RIGHT(LEFT(block, 3), 2)) as sec,
               concat_ws('', CAST(CAST(LEFT(concat_ws('', RIGHT(block, 1), lot), 2) as INTEGER) as varchar(10)), '.', RIGHT(concat_ws('', RIGHT(block, 1), lot), 2)) as block,
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


-------------------------------------------------0600
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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

-------------------------------------------------0700
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(concat_ws('', '00', sub_sec), 2),
                   CASE
                       WHEN LEFT(block, 2) = '00'
                           THEN concat_ws('', RIGHT(concat_ws('', '00', block), 2), '00')
                       ELSE concat_ws('', RIGHT(block, 2), LEFT(block, 2))
                       END, lot, sub_lot) as par_id,
               concat_ws('', CAST(CAST (section AS INTEGER) as varchar(10)), '.', RIGHT(concat_ws('', '00', sub_sec), 2)) as sec,
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

-------------------------------------------------0800
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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

-------------------------------------------------0900
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
    SELECT
           p.muni_code,
           p.parcel_id,
           concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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

-------------------------------------------------1000
INSERT INTO data_source.suffolk_parcel_parid (muni_code, parcel_id, par_id, sec, block, lot, dist_cd, print_key)
    (
        SELECT
               p.muni_code,
               p.parcel_id,
               concat_ws('', RIGHT(concat_ws('', '0000', sw.dist_cd), 4), section, RIGHT(sub_sec, 2), RIGHT(block, 2), '00', lot, sub_lot) as par_id,
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
