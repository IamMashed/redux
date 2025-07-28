
-- add railway into roads table
SELECT setval('roads_id_seq', max(id)) FROM roads;

INSERT INTO roads (osm_id, type, geometry, county)
SELECT osm_id, 'railway', wkb_geometry, county
FROM helper.ways
where other_tags ilike '%"railway"=%';



-- inserting missing broward geometries

WITH helper AS (SELECT pin.*
                FROM property p
                         JOIN helper.broward_gis_label pin ON p.apn = pin.folio
                WHERE p.geo ISNULL)

UPDATE property
SET (latitude, longitude, geo) = (st_x(geometry), --longitude
                                  st_y(geometry),
                                  geometry)
FROM helper
WHERE property.apn = helper.folio;


INSERT INTO property_gis (geometry, property_id, apn, county)
SELECT h.geometry, p.id, p.apn, p.county
FROM helper.broward_gis_polygon h
         JOIN property p ON p.apn = h.folio;

-- updating is_condo for miamidade

UPDATE property
SET is_condo = TRUE
WHERE county = 'miamidade'
  AND condo_view_influence NOTNULL;


-- insert null geo from reference building for miamidade
UPDATE property
SET geo = p2.geo
FROM property p1
         JOIN property p2 ON p1.reference_building = p2.id
WHERE property.geo ISNULL
  AND property.county = 'miamidade'
  AND property.id = p1.id;


-- update assessment_value from value for suffolk and nassau
UPDATE assessment
SET assessment_value = value
FROM property
WHERE property_id = property.id
  AND property.county IN ('suffolk', 'nassau');


--update property_clas_type for nasssau
UPDATE property
SET property_class_type = helper.nassau_property_2021.clas
FROM helper.nassau_property_2021
WHERE county = 'nassau'
  AND property.apn = helper.nassau_property_2021.parid;


-- insert suffolk roads
INSERT INTO roads (osm_id, type, geometry, county)
SELECT osm_id, highway, way, 'suffolk'
FROM helper.planet_osm_roads;


--update owner address lines
UPDATE owner
SET owner_address_2 = initcap(trim(left(owner_address_2, length(owner_address_2) - 7))),
    owner_state = substring(owner_address_2, length(owner_address_2) - 6, 2),
    owner_zip = substring(owner_address_2, length(owner_address_2) - 4, 5)::int,
    owner_address_1 = initcap(owner_address_1),
    owner_address_3 = concat_ws(' ', owner_state, owner_zip),
    owner_city = initcap(owner_city)
WHERE substring(owner_address_2, length(owner_address_2) - 6, 2) = 'FL'
  AND RIGHT(owner_address_2, 5) ~ E'^\\d+$';

-- to test refer to owner property_id's'

-- +-----------+
-- |property_id|
-- +-----------+
-- |892779     |
-- |995771     |
-- |1051592    |
-- |880603     |
-- +-----------+



UPDATE owner
SET owner_address_3 = concat_ws(' ', owner_state, owner_zip)
WHERE length(owner_address_3) = 5
  AND owner_address_3 ~ E'^\\d+$'
  AND owner_state NOTNULL;

-- test property_id's
-- 1218419
-- 1218543
-- 1218599
-- 1218612
-- 1218539
-- 1218581
-- 1218658


UPDATE owner
SET owner_address_3 = concat_ws(' ', owner_state, owner_zip)
WHERE owner_address_3 ILIKE 'FLORIDA _____';

UPDATE owner
SET owner_state = 'FL'
WHERE owner_state = 'FLORIDA';

UPDATE owner
set owner_city = initcap(owner_city),
    owner_address_3 = concat_ws(' ', owner_state, owner_zip),
    owner_address_2 = initcap(owner_city),
    owner_address_1 = initcap(owner_address_1)
WHERE owner_address_3 ISNULL;

UPDATE owner
SET owner_address_3 = owner_address_2,
    owner_address_2 = NULL
WHERE owner_address_3 = ''
  AND RIGHT(owner_address_2, 5) ~ E'^\\d+$';



--move address line 2 to address line 3 if it is only city
UPDATE owner
SET owner_address_3 = format('%s, %s', owner_address_2, owner_address_3),
    owner_address_2 = NULL
WHERE owner_address_2 = owner_city;


--update palmbeach lot size
UPDATE property
SET lot_size = ds.lot_size
FROM data_source.palmbeach_land ds
WHERE property.county = 'palmbeach'
  AND property.apn = ds.apn;

