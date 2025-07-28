-- suffolk

UPDATE property
SET address = concat(loc_st_nbr, ' ', loc_st_name, ' ', loc_mail_st_stuff, ' ', loc_muni_name, ' ', loc_zip)
FROM suffolk_parcel_txt
WHERE property.print_key = suffolk_parcel_txt.print_key
  AND property.street = suffolk_parcel_txt.loc_st_name
  AND property.number = suffolk_parcel_txt.loc_st_nbr
  AND property.county = 'suffolk';

UPDATE property
SET address = rtrim(address, '0000')
WHERE county = 'suffolk';

-- remove multiple spaces
UPDATE property
SET address = trim(regexp_replace(address, '\s+', ' ', 'g'))
WHERE county = 'suffolk';


-- nassau related
UPDATE property
SET address = full_address
FROM nassau_assessment_txt
WHERE property.county = 'nassau'
  AND property.apn = nassau_assessment_txt.parid;


UPDATE property
SET address = trim(regexp_replace(address, '\s+', ' ', 'g'))
WHERE county = 'nassau';

-- miamidade

UPDATE property
SET address = concat(address, ' ', town)
WHERE county = 'miamidade'
  AND town IS NOT NULL
  AND town != '';

UPDATE property
SET address = concat(address, ' ', zip)
WHERE county = 'miamidade'
  AND zip IS NOT NULL;

UPDATE property
SET address = trim(regexp_replace(address, '\s+', ' ', 'g'))
WHERE county = 'miamidade';

-- ROLLBACK changes
UPDATE property
SET address = replace(address, town, '')
WHERE county = 'miamidade'
  AND town IS NOT NULL
  AND town != '';

UPDATE property
SET address = replace(address, zip::varchar, '')
WHERE county = 'miamidade'
  AND zip IS NOT NULL;

UPDATE property
SET address = trim(address)
WHERE county = 'miamidade'


-- custom mass cma ... changing column type
ALTER TABLE nass_sbj
    ALTER property_style TYPE int
        USING CASE property_style
                  WHEN 'RANCH' THEN 1
                  WHEN 'RAISED RANCH/HI RANCH' THEN 2
                  WHEN 'SPLIT LEVEL' THEN 3
                  WHEN 'MODIFIED RANCH' THEN 4
                  WHEN 'CAPE' THEN 5
                  WHEN 'COLONIAL' THEN 6
                  WHEN 'VICTORIAN' THEN 7
                  WHEN 'CONTEMPORARY' THEN 8
                  WHEN 'OLD STYLE' THEN 9
                  WHEN 'BUNGALOW,COTTAGE' THEN 10
                  WHEN 'DUPLEX OR TRIPLEX' THEN 11
                  WHEN 'MANSION, ESTATE' THEN 12
                  WHEN 'TOWNHOUSE' THEN 13
                  WHEN 'CONDO' THEN 14
                  WHEN 'CO-OP' THEN 15
                  WHEN 'HOMOWNER ASSOC' THEN 16
                  WHEN 'OTHER' THEN 17
                  WHEN 'SPLANCH' THEN 18
                  WHEN 'CARRIAGE HOUSE' THEN 19
                  WHEN 'Tudor' THEN 20
                  WHEN 'Store/Dwell' THEN 21
        END;

-- query duplicates
SELECT *
FROM florida_assessment a
WHERE a.ctid <> (SELECT min(b.ctid)
                 FROM florida_assessment b
                 WHERE a.parcel_id = b.parcel_id);
