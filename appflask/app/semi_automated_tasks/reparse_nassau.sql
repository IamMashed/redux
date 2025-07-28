-- insert missing residential

INSERT INTO property(apn, county, school_district, property_class, property_class_type,
                     street, number, state, new_record,
                     address_unit, address_line_1, address_line_2, age,
                     gla_sqft, property_style, garages, basement_type,
                     lot_size, location, full_baths, half_baths, is_condo, town, rooms,
                     fireplaces, heat_type, land_type_code, condo_view_influence)
SELECT "@PARID@",
       'nassau',
       "@SCH@"::int,
       "@LUC@"::int,
       "@CLAS@"::int,
       initcap(concat_ws(' ', "@ADRSTR@", "@ADRSUF@")),
       "@ADRNO@",
       'NY',
       TRUE,
       "@COND@",
       initcap(concat_ws(' ', "@ADRNO@", "@ADRSTR@", "@ADRSUF@")),
       "@COND@",
       "@YRBLT@"::int,
       "@SFLA@"::double precision,
       "@ST@",
       "@BS@"::int,
       "@B@"::int,
       "@ACRES@"::double precision,
       "@LO@"::int,
       "@FIX@"::int,
       "@FIXX@"::int,
       "@COND@" NOTNULL AND "@COND@" != '',
       (SELECT CASE
                   WHEN "@T@" = '1' THEN 'Hempstead'
                   WHEN "@T@" = '2' THEN 'North Hempstead'
                   WHEN "@T@" = '3' THEN 'Oyster Bay'
                   WHEN "@T@" = '4' THEN 'Glen Cove'
                   WHEN "@T@" = '5' THEN 'Long Beach' END
       ),
       "@RMT@"::int,
       "@WBF@"::int,
       "@H@",
       "@COD@",
       "@CON_1@"
FROM data_source.nassau_property_residential
ON CONFLICT DO NOTHING
;

--update records
UPDATE property
SET (school_district, property_class, property_class_type,
     street, number, state,
     address_unit, address_line_1, address_line_2, age,
     garages,
     town, rooms,
     fireplaces, heat_type, land_type_code, condo_view_influence)=
        (
         "@SCH@"::int,
         "@LUC@"::int,
         "@CLAS@"::int,
         trim(initcap(concat_ws(' ', "@ADRSTR@", "@ADRSUF@"))),
         "@ADRNO@",
         'NY',
         "@COND@",
         trim(initcap(concat_ws(' ', "@ADRNO@", "@ADRSTR@", "@ADRSUF@"))),
         "@COND@",
         "@YRBLT@"::int,
         "@BS@"::int,
         (SELECT CASE
                     WHEN "@T@" = '1' THEN 'Hempstead'
                     WHEN "@T@" = '2' THEN 'North Hempstead'
                     WHEN "@T@" = '3' THEN 'Oyster Bay'
                     WHEN "@T@" = '4' THEN 'Glen Cove'
                     WHEN "@T@" = '5' THEN 'Long Beach' END
         ),
         "@RMT@"::int,
         "@WBF@"::int,
         "@H@",
         "@COD@",
         "@CON_1@")
FROM data_source.nassau_property_residential ds
WHERE ds."@PARID@" = property.apn
and property.county = 'nassau'
;

--update zip and city
UPDATE property
SET (zip, city) = (
                   right(property_address_2, 5)::int,
                   trim(initcap(left(property_address_2, -5)))
                  )
FROM data_source.nassau_assessment ds
WHERE RIGHT(property_address_2, 5) ~ E'^\\d+$'
  AND county = 'nassau'
  AND property.apn = ds.parid;


--update address lines

UPDATE property
SET address_line_2 = NULL
WHERE county = 'nassau'
  AND trim(address_line_2) = '';

UPDATE property
SET address_line_1 = trim(address_line_1)
WHERE county = 'nassau';


--update address unit

UPDATE property
SET address_unit = NULL
WHERE county = 'nassau'
  AND trim(address_unit) = '';


UPDATE property
SET address_line_2 = nullif(concat_ws(' ', 'Unit', address_unit), 'Unit'),
    address_line_1 = initcap(address_line_1)
WHERE county = 'nassau';


--update address

UPDATE property
SET address =
        concat_ws(', ', address_line_1, address_line_2, city, concat_ws(' ', state, zip))
WHERE county = 'nassau';

--update lat lon

UPDATE property
SET longitude = st_x(geo),
    latitude  = st_y(geo)
WHERE county = 'nassau'
  AND geo NOTNULL
  AND (latitude ISNULL OR longitude ISNULL);


-- update new records from nass sbj. Commented out as no longer used.

-- UPDATE property
-- SET section        = ds.section,
--     block          = ds.block,
--     lot            = ds.lot,
--     lot_size       = ds.lot_size,
--     rooms          = ds.rooms,
--     gla_sqft       = ds.gla_sqft,
--     basement_type  = ds.basement_type,
--     waterfront     = (SELECT CASE WHEN ds.waterfront = 'Y' THEN TRUE END),
--     garages        = ds.no_cars,
--     property_style = ds.property_style,
--     full_baths     = ds.full_baths,
--     half_baths     = ds.half_baths,
--     location       = ds.location
-- FROM data_source.nass_sbj ds
-- WHERE property.new_record = TRUE
--   AND property.county = 'nassau'
--   AND property.apn = ds.apn
-- ;

-- insert new assessment date
INSERT INTO assessment_dates (id, county, assessment_type, tax_year, valuation_date, assessment_name, release_date)
VALUES (DEFAULT, 'nassau', 1, 2020, '2020-08-25', 'Final ''20', '2020-08-25');


-- insert new assessments...check new assessment date id before running below command

INSERT INTO assessment (value, assessment_type, property_id, swiss_code, village_1, village_1_pct, village_2,
                        village_2_pct, village_3, village_3_pct, assessment_id, override_value, assessment_value)
    (SELECT ds.total_assessment,
            'final',
            (SELECT id FROM property WHERE apn = ds.parid),
            ds.swiss_code,
            ds.village_1,
            ds.village_1_pct::double precision,
            ds.village_2,
            ds.village_2_pct::double precision,
            ds.village_3,
            ds.village_3_pct::double precision,
            9,
            NULL,
            ds.total_assessment
     FROM data_source.nassau_assessment ds
              JOIN property p ON ds.parid = p.apn);


-- update is_residential
UPDATE property p
SET is_residential = TRUE
WHERE p.county = 'nassau'
  AND ((p.property_class = 2100 AND p.property_class_type = 1)
    OR (p.property_class = 2102 AND p.property_class_type = 1)
    OR (p.property_class = 2150 AND p.property_class_type = 1)
    OR (p.property_class = 2200 AND p.property_class_type = 1)
    OR (p.property_class = 2300 AND p.property_class_type = 1)
    OR (p.property_class = 2400 AND p.property_class_type = 1)
    OR (p.property_class = 2500 AND p.property_class_type = 1)
    OR (p.property_class = 2600 AND p.property_class_type = 1)
    OR (p.property_class = 2800 AND p.property_class_type = 1)
    OR (p.property_class = 4122 AND p.property_class_type = 1)
    OR (p.property_class = 4830 AND p.property_class_type = 1));



-- drop taken from nass_sbj
-- just in case run the update again.
UPDATE property
SET lot_size       = (SELECT CASE
                                 WHEN "@ACRES@" = '' THEN NULL
                                 ELSE "@ACRES@"::double precision END),
    gla_sqft       = (SELECT CASE
                                 WHEN "@SFLA@" = '' THEN NULL
                                 ELSE "@SFLA@"::double precision END),
    rooms          = (SELECT CASE WHEN "@RMT@" = '' THEN NULL ELSE "@RMT@"::INT END),
    basement_type  = (SELECT CASE WHEN "@B@" = '' THEN NULL ELSE "@B@"::INT END),
    full_baths     = (SELECT CASE WHEN "@FIX@" = '' THEN NULL ELSE "@FIX@"::INT END),
    half_baths     = (SELECT CASE WHEN "@FIXX@" = '' THEN NULL ELSE "@FIXX@"::INT END),
    property_style = (SELECT CASE WHEN "@ST_1@" = '' THEN NULL ELSE "@ST_1@"::INT::TEXT END),
    LOCATION       = (SELECT CASE WHEN "@LO@" = '' THEN NULL ELSE "@LO@"::INT END)
FROM data_source.nassau_property_residential ds
WHERE ds."@PARID@" = property.apn
  AND property.county = 'nassau';

-- update garages and waterfront

UPDATE property
SET garages = garage_number
FROM (
         WITH vector_sub AS (SELECT sbl       AS apn,
                                    sum(area) AS vector_sum
                             FROM data_source.nassau_residential_vector ds
                             WHERE first = '13'
                             GROUP BY sbl),

              other_building_sub AS (SELECT "@PARID@"                                                   AS apn,
                                            (CASE WHEN "@AREA_1@" = '' THEN 0 ELSE "@AREA_1@"::int END) +
                                            (CASE WHEN "@AREA_2@" = '' THEN 0 ELSE "@AREA_2@"::int END) +
                                            (CASE WHEN "@AREA_3@" = '' THEN 0 ELSE "@AREA_3@"::int END) +
                                            (CASE WHEN "@AREA_4@" = '' THEN 0 ELSE "@AREA_4@"::int END) +
                                            (CASE WHEN "@AREA_5@" = '' THEN 0 ELSE "@AREA_5@"::int END) +
                                            (CASE WHEN "@AREA_6@" = '' THEN 0 ELSE "@AREA_6@"::int END) AS other_buildings_sum
                                     FROM data_source.nassau_property_residential ds
                                     WHERE ("@COD_1@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                         OR "@COD_2@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                         OR "@COD_3@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                         OR "@COD_4@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                         OR "@COD_5@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                         OR "@COD_6@" IN ('RG1', 'RG2', 'RA1', 'RA2')
                                               )
              )
         SELECT obs.apn                   AS apn_1,
                vs.apn                    AS apn_2,
                coalesce(obs.apn, vs.apn) AS apn,
                other_buildings_sum,
                vector_sum,
                greatest(other_buildings_sum, vector_sum),
                (CASE
                     WHEN greatest(other_buildings_sum, vector_sum) BETWEEN 0 AND 399 THEN 1
                     WHEN greatest(other_buildings_sum, vector_sum) BETWEEN 400 AND 599 THEN 2
                     WHEN greatest(other_buildings_sum, vector_sum) BETWEEN 600 AND 799 THEN 3
                     WHEN greatest(other_buildings_sum, vector_sum) BETWEEN 800 AND 999 THEN 4
                     ELSE 0 END)          AS garage_number
         FROM other_building_sub obs
                  FULL OUTER JOIN vector_sub vs ON vs.apn = obs.apn) foo
WHERE foo.apn = property.apn
  AND property.county = 'nassau'
;


UPDATE property
SET garages = 0
WHERE garages ISNULL
  AND county IN ('nassau', 'suffolk');


UPDATE property
SET waterfront = (CASE WHEN "@COD@" IN ('2', '2B', '2C', '2L', '2O', '2S', '2L') THEN TRUE ELSE FALSE END)
FROM data_source.nassau_property_residential ds
WHERE ds."@PARID@" = property.apn
  AND property.county = 'nassau';


--update nassau owner
UPDATE owner o
SET owner_address_1 = initcap(owner_address_1),
    owner_address_2 = initcap(owner_address_2),
    owner_address_3 = format('%s,%s', initcap(left(o.owner_address_3, -9)), right(o.owner_address_3, 9)),
    owner_city      = initcap(owner_city)
FROM property p
WHERE o.property_id = p.id
  AND p.county = 'nassau'
  AND o.data_source = 'assessment'
  AND o.owner_address_3 ILIKE '% __ _____'
  AND RIGHT(o.owner_address_3, 5) ~ E'^\\d+$';


--update nassau address
UPDATE property
SET address = replace(address, ' Ny,NY', ',NY')
WHERE county = 'nassau'
  AND address ILIKE '% ny,ny %'