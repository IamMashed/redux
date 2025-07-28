--insert new properties from parcel.txt, res_bldg.txt, suffolk_parcel_parid
INSERT INTO property (apn, county, section, block, lot, number, street, town, state, zip, coordinate_x, coordinate_y,
                      undefined_field, print_key,
                      property_style,  gla_sqft, story_height, age, basement_type, full_baths,
                      half_baths, rooms, bedrooms, kitchens, fireplaces, heat_type, condition, effective_age,
                      new_record)
    (SELECT spp.par_id,
            'suffolk',

            -- from parcel.txt
            sp.section,
            sp.block,
            sp.lot,
            sp.loc_st_nbr,
            sp.loc_st_name,
            sp.loc_muni_name,
            'NY',
            left(sp.loc_zip, 5)::int,
            sp.grid_east,
            sp.grid_north,
            sp.muni_code,
            sp.print_key,

            -- from res_bldg.txt
            rsbld.bldg_style,
            rsbld.sqft_living_area,
            rsbld.nbr_stories,
            rsbld.yr_blt,
            rsbld.bsmnt_type,
            rsbld.nbr_full_baths::int,
            rsbld.nbr_half_baths::int,
            rsbld.nbr_rooms::int,
            rsbld.nbr_bed::int,
            rsbld.nbr_kitchens::int,

            rsbld.nbr_fireplaces::int,
            rsbld.heat_type,
            rsbld.interior_cond,
            rsbld.yr_remodeled, -- effective age???
            TRUE              --new_record
     FROM suffolk_res_bldg  rsbld
         join suffolk_parcel sp on (rsbld.muni_code = sp.muni_code and rsbld.parcel_id = sp.parcel_id)
         join suffolk_parcel_parid spp on (spp.muni_code = sp.muni_code and spp.parcel_id=sp.parcel_id)
         left join property p on spp.par_id = p.apn
    WHERE p.apn is null

    )
ON CONFLICT DO NOTHING
;

-- update from 'suff_output_res_bldg' re-parsed
UPDATE property
SET (section, block, lot, number, street, town, state, zip, coordinate_x, coordinate_y,
     undefined_field, print_key, property_style,  gla_sqft, story_height, age, basement_type, full_baths,
     half_baths, rooms, bedrooms, kitchens, fireplaces, heat_type, condition, effective_age, address_line_1,
    address_line_2, address) =
    (
     rsbld.section, rsbld.block, rsbld.lot, rsbld.number, rsbld.street, rsbld.town,
     rsbld.state, rsbld.zip::int, rsbld.coordinate_x, rsbld.coordinate_y, rsbld.undefined_field, rsbld.print_key,
     rsbld.property_style, rsbld.gla_sqft, rsbld.story_height, rsbld.age, rsbld.basement_type, rsbld.full_baths,
     rsbld.half_baths, rsbld.rooms, rsbld.bedrooms, rsbld.kitchens, rsbld.fireplaces, rsbld.heat_type,
     rsbld.condition, rsbld.effective_age, rsbld.address_line_1, rsbld.address_line_2, rsbld.address
    )
FROM data_source.suff_output_res_bldg  rsbld
WHERE property.apn = rsbld.apn
AND property.county = 'suffolk';



update public.property
set (address, address_line_1) =
    (
        btrim(trim(regexp_replace(addr.address, '\s+', ' ', 'g'))),
        btrim(trim(regexp_replace(addr.addr_line_1, '\s+', ' ', 'g')))
    )
from data_source.addresses_suffolk_property_df addr
where apn = addr.par_id
and county='suffolk';


update public.property p
set (address, address_line_1) =
    (
        btrim(trim(regexp_replace(addr.address, '\s+', ' ', 'g'))),
        btrim(trim(regexp_replace(addr.address_line_1, '\s+', ' ', 'g')))
    )
from data_source.suff_output_res_bldg addr
where p.apn = addr.apn
and p.county='suffolk';


-- update street number zip
UPDATE property
SET (number, street, state, zip, address_unit) =
        (btrim(sp.loc_st_nbr),
         btrim(trim(regexp_replace(sp.loc_st_name, '\s+', ' ', 'g'))),
         'NY',
         left(sp.loc_zip, 5)::int,
         concat_ws(' ', sp.loc_unit_name, sp.loc_unit_nbr)
            )
FROM suffolk_parcel sp
    join suffolk_parcel_parid spp on (sp.muni_code = spp.muni_code and sp.parcel_id = spp.parcel_id)
    join property p on spp.par_id = p.apn
where property.apn in (
    select spp.par_id from suffolk_parcel_parid spp
                join suffolk_res_bldg srb on (spp.muni_code = srb.muni_code and srb.parcel_id=spp.parcel_id)
    );
--======================================================================================================================

--insert new properties from suff priv inv
INSERT INTO property (apn, county, property_style, lot_size, gla_sqft, story_height,
                      age, basement_type, full_baths,
                      half_baths, garages, rooms, bedrooms, kitchens, pool, waterfront,
                      fireplaces, new_record)
    (SELECT apn,
            'suffolk',
            style,
            lot_size,
            gla,
            height,
            age,
            (SELECT CASE
                        WHEN lower(basement) = 'none' THEN '0'
                        WHEN lower(basement) = 'slab' THEN '1'
                        WHEN lower(basement) = 'crawl' THEN '2'
                        WHEN lower(basement) = 'half' THEN '3'
                        WHEN lower(basement) = 'full' THEN '4'
                        WHEN lower(basement) = 'pier' THEN '5'
                        WHEN lower(basement) = 'partial' THEN '6'
                        WHEN lower(basement) = 'part' THEN '7'
                        WHEN lower(basement) = '' THEN NULL
                        END)::int,
            floor(baths),     --full_baths
            (SELECT CASE
                        WHEN floor(baths) != baths THEN 1
                        WHEN floor(baths) = baths THEN 0
                        END), --half_baths
            garage,
            rooms::int,
            bedrooms::int,
            kitchens,
            (SELECT CASE
                        WHEN btrim(pool) = 'Y' THEN TRUE
                        WHEN btrim(pool) = 'N' THEN FALSE
                        END),
            (SELECT CASE
                        WHEN btrim(waterfront) = 'Y' THEN TRUE
                        WHEN btrim(waterfront) = 'N' THEN FALSE
                        END),
            fireplaces::int,
            TRUE              --new_record
     FROM data_source.suffolk_priv_inv
    )
ON CONFLICT DO NOTHING
;

--update new properties from suff priv inv
UPDATE property
SET (county, property_style, lot_size, gla_sqft, story_height,
     age, basement_type, full_baths,
     half_baths, garages, rooms, bedrooms, kitchens, pool, waterfront,
     fireplaces, new_record) =
        ('suffolk',
         ds.style,
         ds.lot_size,
         ds.gla,
         ds.height,
         ds.age,
         (SELECT CASE
                     WHEN lower(basement) = 'none' THEN '0'
                     WHEN lower(basement) = 'slab' THEN '1'
                     WHEN lower(basement) = 'crawl' THEN '2'
                     WHEN lower(basement) = 'half' THEN '3'
                     WHEN lower(basement) = 'full' THEN '4'
                     WHEN lower(basement) = 'pier' THEN '5'
                     WHEN lower(basement) = 'partial' THEN '6'
                     WHEN lower(basement) = 'part' THEN '7'
                     WHEN lower(basement) = '' THEN NULL
                     END)::int,
         floor(baths), --full_baths
         (SELECT CASE
                     WHEN floor(baths) != baths THEN 1
                     WHEN floor(baths) = baths THEN 0
                     END), --half_baths
         garage,
         ds.rooms::int,
         ds.bedrooms::int,
         ds.kitchens,
         (SELECT CASE
                     WHEN btrim(ds.pool) = 'Y' THEN TRUE
                     WHEN btrim(ds.pool) = 'N' THEN FALSE
                     END),
         (SELECT CASE
                     WHEN btrim(ds.waterfront) = 'Y' THEN TRUE
                     WHEN btrim(ds.waterfront) = 'N' THEN FALSE
                     END),
         ds.fireplaces::int,
         TRUE --new_record
            )
FROM data_source.suffolk_priv_inv ds
WHERE ds.apn = property.apn
  AND property.county = 'suffolk'
  AND new_record = TRUE
;

--update lot block

UPDATE property
SET (section, block, lot, print_key, school_district, undefined_field) = (sec, s.block, s.lot, s.print_key, muni_code, parcel_id)
FROM suffolk.parcel_parid s
WHERE county = 'suffolk'
  AND s.par_id = apn
  AND new_record = TRUE;

-- update street number zip
UPDATE property
SET (number, street, state, zip, undefined_field, address_unit) =
        (btrim(loc_st_nbr),
         btrim(trim(regexp_replace(loc_st_name, '\s+', ' ', 'g'))),
         'NY',
         left(loc_zip, 5)::int,
         parcel_id,
         concat_ws(' ', loc_unit_name, loc_unit_nbr)
            )
FROM suffolk.parcel s
WHERE county = 'suffolk'
  AND new_record = TRUE
  AND s.print_key = property.print_key
  AND muni_code = school_district;

--update street
UPDATE property
SET street = initcap(street)
WHERE county = 'suffolk';

UPDATE property
SET street = btrim(regexp_replace(street, '\s+', ' ', 'g'))
WHERE county = 'suffolk';


-- add helper muni_code field to be used to map suffolk data
ALTER TABLE property
    ADD muni_code int;


UPDATE property
SET (muni_code, print_key) = (s.muni_code, s.print_key)
FROM suffolk.parcel_parid s
WHERE s.par_id = property.apn
  AND property.county = 'suffolk';


UPDATE property
SET (section, block, lot) = (s.sec, s.block, s.lot)
FROM suffolk.parcel_parid s
WHERE s.par_id = property.apn
  AND new_record = FALSE;


UPDATE property
SET undefined_field = parcel_id
FROM suffolk.parcel s
WHERE county = 'suffolk'
  AND s.print_key = property.print_key
  AND s.muni_code = property.muni_code;


--update city

UPDATE property
SET city = initcap(loc_muni_name)
FROM suffolk.parcel s
WHERE county = 'suffolk'
  AND s.parcel_id = property.undefined_field::int
  AND s.print_key = property.print_key

--update address lines

UPDATE property
SET address_line_1 =
        initcap(concat_ws(' ', loc_st_nbr, loc_prefix_dir, loc_st_name, loc_mail_st_suff))
FROM suffolk.parcel s
WHERE s.parcel_id = property.undefined_field::int
  AND s.print_key = property.print_key
  AND county = 'suffolk';

UPDATE property
SET address_line_2 =
        nullif(initcap(concat_ws(' ', loc_unit_name, loc_unit_nbr)), '')
FROM suffolk.parcel s
WHERE s.parcel_id = property.undefined_field::int
  AND s.print_key = property.print_key
  AND county = 'suffolk';


UPDATE property
SET address_unit =
        nullif(initcap(concat_ws(' ', loc_unit_name, loc_unit_nbr)), '')
FROM suffolk.parcel s
WHERE county = 'suffolk'
  AND s.parcel_id = property.undefined_field::int
  AND s.print_key = property.print_key
  AND (address_unit ISNULL OR address_unit = '');


UPDATE property
SET (zip, address_line_1) =
        (left(zip::text, 5)::int,
         btrim(regexp_replace(address_line_1, '\s+', ' ', 'g')))
WHERE county = 'suffolk';


--update address

UPDATE property
SET address =
        concat_ws(',', address_line_1, address_line_2, city, concat_ws(' ', state, zip))
WHERE county = 'suffolk';


update property set undefined_field = null where trim(undefined_field) = '';
alter table property alter column undefined_field type int using undefined_field::int;


-- insert assessments from parsed suff_assessment.csv file
INSERT INTO assessment (value, assessment_type, property_id, assessment_id, assessment_value)
    (
        SELECT
               a.total_av,
               a.assessment_type,
               p.id,
               a.assessment_id,
               a.total_av
        FROM data_source.suff_assessment a JOIN property p on a.par_id=p.apn
    )
ON CONFLICT DO NOTHING
;

-- update property_class, school_district from assessment
update property p
set (property_class, school_district)= (a.prop_class, a.sch_code)
from data_source.suff_assessment a
where p.apn=a.par_id;














