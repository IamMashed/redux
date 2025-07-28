-- noinspection SqlNoDataSourceInspectionForFile

-- create point_4326 geometry(Point, 4326) in helper.dade_2019pin

UPDATE helper.dade_2019pin
SET centroid = st_centroid(geom_4326);

-- auto-generated definition
CREATE TABLE dade_point
(
    gid        serial NOT NULL
        CONSTRAINT dade_point_pk
            PRIMARY KEY,
    parcelno   varchar(17),
    point_4326 geometry(Point, 4326)
);

COMMENT ON TABLE dade_point IS 'point geometry for dade properties derived from multipolygon';

ALTER TABLE dade_point
    OWNER TO postgres;

CREATE UNIQUE INDEX dade_point_parcelno_uindex
    ON dade_point (parcelno);

ALTER TABLE dade_point
    SET SCHEMA helper;


INSERT INTO helper.dade_point(parcelno, point_4326)
SELECT parcelno, st_centroid(st_collect(centroid))
FROM helper.dade_2019pin
GROUP BY 1;

UPDATE property
SET geo = pp.point_4326
FROM helper.dade_point pp
WHERE property.apn = pp.parcelno
  AND property.geo IS NULL
  AND property.county = 'dade';

-- check if upper succeeded
SELECT count(*)
FROM property
WHERE county = 'dade'
  AND geo IS NULL;


-- update polyfgons from property_gis table
INSERT INTO property_gis(geometry, property_id, apn, county)
SELECT geom_4326, p.id, p.apn, p.county
FROM helper.dade_2019pin
         JOIN property p ON parcelno = p.apn
         LEFT JOIN property_gis pg ON p.id = pg.property_id
WHERE pg.property_id IS NULL;

-- check if updated
WITH gis AS (SELECT count(*), property_id FROM property_gis GROUP BY property_id)
SELECT count(*)
FROM property p
         JOIN gis ON gis.property_id = p.id
WHERE p.county = 'dade';


SELECT count(*)
FROM helper.dade_2019pin;
SELECT count(*)

FROM property
WHERE county = 'dade';


-- miamidade reference building
WITH bar AS (WITH foo AS (SELECT left(apn, length(apn) - 4) || '0001' AS apn, count(*)
                          FROM property
                          WHERE county = 'miamidade'
                            AND is_condo = TRUE
                            AND geo IS NULL
                          GROUP BY 1
                          ORDER BY 1)

             SELECT foo.apn AS foo_apn, is_condo, geo, p.id AS p_id
             FROM foo
                      JOIN property p ON p.apn = foo.apn
             WHERE geo IS NOT NULL)

UPDATE property p
SET reference_building = p_id
FROM bar
WHERE left(foo_apn, length(foo_apn) - 4) = left(p.apn, length(p.apn) - 4)
AND p.geo IS NULL;



-- use property_gis to update palmbeach latitude and longitude

WITH helper AS (SELECT p.id, st_centroid(st_collect(pg.geometry)) AS center
                FROM property p
                         JOIN property_gis pg ON p.id = pg.property_id
                WHERE p.county = 'palmbeach'
                  AND p.latitude IS NULL
                  AND p.geo IS NOT NULL
                GROUP BY p.id),
     lat_lon AS (SELECT id, st_x(center) AS lon, st_y(center) AS lat
                 FROM helper)
UPDATE property
SET latitude  = lat_lon.lat,
    longitude = lat_lon.lon
FROM lat_lon
WHERE property.county = 'palmbeach'
  AND property.latitude IS NULL
  AND property.id = lat_lon.id;


-- extract lat and lot from geometry
UPDATE property
SET longitude = st_x(st_transform(st_setsrid(geo, 2881), 4326)),
    latitude  = st_y(st_transform(st_setsrid(geo, 2881), 4326))
WHERE county = 'miamidade'
  AND latitude IS NULL
  AND geo NOTNULL


-- extract lat and lon from reference building
WITH rf AS (SELECT p1.reference_building, p.latitude, p.longitude
            FROM property p1
                     JOIN property p ON p.id = p1.reference_building
            WHERE p1.county = 'miamidade'
              AND p1.latitude IS NULL
              AND p1.reference_building NOTNULL)
UPDATE property
SET latitude  = rf.latitude,
    longitude = rf.longitude
FROM rf
WHERE county = 'miamidade'
  AND property.latitude IS NULL
  AND property.reference_building NOTNULL
  AND rf.reference_building = property.reference_building

--update property_gis with valid geometry srid
UPDATE property_gis
SET geometry = st_transform(st_setsrid(geometry, 2881), 4326)
WHERE county = 'broward'
  AND st_x(st_centroid(geometry)) > 900;


SELECT count(*)
FROM obsolescences
GROUP BY obs_id

SELECT DISTINCT st_srid(geometry)
FROM property_gis
WHERE county = 'palmbeach'

SELECT DISTINCT st_srid(geo)
FROM property
WHERE county = 'palmbeach'

SELECT st_x(st_centroid(geometry)), property_id, geometry
FROM property_gis
WHERE county = 'palmbeach'
  AND st_srid(geometry) = 0

SELECT st_x(st_centroid(geo)), id, geo
FROM property
WHERE county = 'palmbeach'
  AND st_srid(geo) = 0

select st_transform(st_setsrid(geometry, 2881), 4326) from property_gis where property_id = 4363657

update property_gis set geometry = st_transform(st_setsrid(geometry, 2881), 4326) where county = 'palmbeach'
and st_x(st_centroid(geometry))>100;

update property_gis set geometry = st_setsrid(geometry, 4326) where county = 'palmbeach'
and st_srid(geometry) = 0;

UPDATE property
SET geo = st_setsrid(geo, 4326)
WHERE county = 'palmbeach'
  AND st_srid(geo) = 0;


--update missing property geo from st_centroid(st_union(property_gis geometry))
WITH foo AS (SELECT p.id, p.geo, st_centroid(st_union(pg.geometry))
             FROM property p
                      LEFT JOIN property_gis pg ON p.id = pg.property_id
             WHERE p.county = 'nassau'
               AND p.geo ISNULL
               AND pg.geometry NOTNULL
             GROUP BY 1, 2)
UPDATE property
SET geo = foo.st_centroid
FROM foo
WHERE property.id = foo.id