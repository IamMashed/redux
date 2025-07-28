-- insert missing broward records

WITH helper AS (SELECT h.*, p.apn AS apn
                FROM helper.bcpa_tax_roll_ib_july_2020_final h
                         LEFT JOIN property p ON h.folio_number = p.apn
                WHERE apn ISNULL
)
INSERT
INTO property(apn, county, section, block, lot, address, address_line_1, address_line_2, address_unit, street, number,
              town, city, state, zip, is_condo, waterfront,
              property_class, age, gla_sqft, under_air_gla_sqft, full_baths, half_baths, bedrooms, property_style,
              price_per_sqft, lot_size, location, land_use, land_tag)
SELECT folio_number,
       'broward',
       substring(folio_number, 5, 2),
       substring(folio_number, 7, 2),
       substring(folio_number, 9, 3),
       concat_ws(' ', nullif(concat_ws(' - ', situs_street_number, situs_street_number_end), ''),
                 situs_street_direction, situs_street_name, situs_street_type, situs_street_post_dir,
                 NULLIF(concat('#', situs_unit_number), '#'), concat(situs_city, ','), situs_zip_code),
       concat_ws(' ', nullif(concat_ws(' - ', situs_street_number, situs_street_number_end), ''),
                 situs_street_direction, situs_street_name, situs_street_type, situs_street_post_dir),
       NULLIF(concat_ws(' ', 'UNIT', situs_unit_number), 'UNIT'),
       situs_unit_number,
       situs_street_name,
       situs_street_number,
       (SELECT CASE
                   WHEN situs_city = 'BC' THEN 'UNINCORPORATED'
                   WHEN situs_city = 'CK' THEN 'COCONUT CREEK'
                   WHEN situs_city = 'CS' THEN 'CORAL SPRINGS'
                   WHEN situs_city = 'CY' THEN 'COOPER CITY'
                   WHEN situs_city = 'DB' THEN 'DEERFIELD BEACH'
                   WHEN situs_city = 'DN' THEN 'DANIA BEACH'
                   WHEN situs_city = 'DV' THEN 'DAVIE'
                   WHEN situs_city = 'FL' THEN 'FORT LAUDERDALE'
                   WHEN situs_city = 'HA' THEN 'HALLANDALE BEACH'
                   WHEN situs_city = 'HB' THEN 'HILLSBORO BEACH'
                   WHEN situs_city = 'HW' THEN 'HOLLYWOOD'
                   WHEN situs_city = 'LH' THEN 'LAUDERHILL'
                   WHEN situs_city = 'LL' THEN 'LAUDERDALE LAKES'
                   WHEN situs_city = 'LP' THEN 'LIGHTHOUSE POINT'
                   WHEN situs_city = 'LS' THEN 'LAUD BY THE SEA'
                   WHEN situs_city = 'LZ' THEN 'LAZY LAKE'
                   WHEN situs_city = 'MG' THEN 'MARGATE'
                   WHEN situs_city = 'MM' THEN 'MIRAMAR'
                   WHEN situs_city = 'NL' THEN 'NORTH LAUDERDALE'
                   WHEN situs_city = 'OP' THEN 'OAKLAND PARK'
                   WHEN situs_city = 'PA' THEN 'PARKLAND'
                   WHEN situs_city = 'PB' THEN 'POMPANO BEACH'
                   WHEN situs_city = 'PI' THEN 'PEMBROKE PINES'
                   WHEN situs_city = 'PK' THEN 'PEMBROKE PARK'
                   WHEN situs_city = 'PL' THEN 'PLANTATION'
                   WHEN situs_city = 'SL' THEN 'SEA RANCH LAKES'
                   WHEN situs_city = 'SU' THEN 'SUNRISE'
                   WHEN situs_city = 'SW' THEN 'SOUTHWEST RANCHES'
                   WHEN situs_city = 'TM' THEN 'TAMARAC'
                   WHEN situs_city = 'WM' THEN 'WILTON MANORS'
                   WHEN situs_city = 'WP' THEN 'WEST PARK'
                   WHEN situs_city = 'WS' THEN 'WESTON' END),
       (SELECT CASE
                   WHEN situs_city = 'BC' THEN 'UNINCORPORATED'
                   WHEN situs_city = 'CK' THEN 'COCONUT CREEK'
                   WHEN situs_city = 'CS' THEN 'CORAL SPRINGS'
                   WHEN situs_city = 'CY' THEN 'COOPER CITY'
                   WHEN situs_city = 'DB' THEN 'DEERFIELD BEACH'
                   WHEN situs_city = 'DN' THEN 'DANIA BEACH'
                   WHEN situs_city = 'DV' THEN 'DAVIE'
                   WHEN situs_city = 'FL' THEN 'FORT LAUDERDALE'
                   WHEN situs_city = 'HA' THEN 'HALLANDALE BEACH'
                   WHEN situs_city = 'HB' THEN 'HILLSBORO BEACH'
                   WHEN situs_city = 'HW' THEN 'HOLLYWOOD'
                   WHEN situs_city = 'LH' THEN 'LAUDERHILL'
                   WHEN situs_city = 'LL' THEN 'LAUDERDALE LAKES'
                   WHEN situs_city = 'LP' THEN 'LIGHTHOUSE POINT'
                   WHEN situs_city = 'LS' THEN 'LAUD BY THE SEA'
                   WHEN situs_city = 'LZ' THEN 'LAZY LAKE'
                   WHEN situs_city = 'MG' THEN 'MARGATE'
                   WHEN situs_city = 'MM' THEN 'MIRAMAR'
                   WHEN situs_city = 'NL' THEN 'NORTH LAUDERDALE'
                   WHEN situs_city = 'OP' THEN 'OAKLAND PARK'
                   WHEN situs_city = 'PA' THEN 'PARKLAND'
                   WHEN situs_city = 'PB' THEN 'POMPANO BEACH'
                   WHEN situs_city = 'PI' THEN 'PEMBROKE PINES'
                   WHEN situs_city = 'PK' THEN 'PEMBROKE PARK'
                   WHEN situs_city = 'PL' THEN 'PLANTATION'
                   WHEN situs_city = 'SL' THEN 'SEA RANCH LAKES'
                   WHEN situs_city = 'SU' THEN 'SUNRISE'
                   WHEN situs_city = 'SW' THEN 'SOUTHWEST RANCHES'
                   WHEN situs_city = 'TM' THEN 'TAMARAC'
                   WHEN situs_city = 'WM' THEN 'WILTON MANORS'
                   WHEN situs_city = 'WP' THEN 'WEST PARK'
                   WHEN situs_city = 'WS' THEN 'WESTON' END),
       'FL',
       situs_zip_code,
       (SELECT CASE WHEN substring(folio_number, 7, 1) ~ E'^\\d+$' THEN FALSE ELSE TRUE END),
       (SELECT CASE
                   WHEN land_tag BETWEEN 1 AND 16 THEN TRUE
                   WHEN land_tag IN (24, 25, 26, 28, 62, 63, 64) THEN TRUE
                   WHEN land_tag BETWEEN 77 AND 86 THEN TRUE
                   ELSE FALSE
                   END),
       use_code,
       (SELECT CASE
                   WHEN actual_year_built = 0 THEN NULL
                   WHEN actual_year_built != 0 THEN actual_year_built END),
       bldg_adj_sq_footage,
       bldg_under_air_sq_footage,
       floor(baths),
       (SELECT CASE
                   WHEN floor(baths) NOTNULL AND floor(baths) != 0 THEN mod(baths, floor(baths))
                   WHEN floor(baths) = 0 THEN 1
                   END),
       beds,
       bldg_cclass::varchar,
       h.land_calc_prc_per_fact_unit_1,
       round(h.land_calc_fact_1 / 43560, 3),
       left(millage_code::varchar, 2)::int,
       use_code,
       land_tag
FROM helper.bcpa_tax_roll_ib_july_2020_final h;


-- update existing properties
UPDATE property
SET (apn, county, section, block, lot, address, address_line_1, address_line_2, address_unit, street, number,
     town, city, state, zip, is_condo, waterfront,
     property_class, age, gla_sqft, under_air_gla_sqft, full_baths, half_baths, bedrooms, property_style,
     price_per_sqft, lot_size, location, land_use, land_tag, lot_size_sqft) =
        (folio_number,
         'broward',
         substring(folio_number, 5, 2),
         substring(folio_number, 7, 2),
         substring(folio_number, 9, 3),
         concat_ws(
                ', ',
                concat_ws(' ',
                          NULLIF(concat_ws(' - ', situs_street_number, situs_street_number_end), ''),
                          situs_street_direction,
                          (SELECT CASE
                                      WHEN TRIM(situs_street_name) ~ E'^\\d+$' AND RIGHT(TRIM(street), 1) = '1'
                                          THEN concat(situs_street_name, 'st')
                                      WHEN TRIM(situs_street_name) ~ E'^\\d+$' AND RIGHT(TRIM(street), 1) = '2'
                                          THEN concat(situs_street_name, 'nd')
                                      WHEN TRIM(situs_street_name) ~ E'^\\d+$' AND RIGHT(TRIM(street), 1) = '3'
                                          THEN concat(situs_street_name, 'rd')
                                      WHEN TRIM(situs_street_name) ~ E'^\\d+$' AND
                                           RIGHT(TRIM(street), 1) NOT IN ('1', '2', '3')
                                          THEN concat(situs_street_name, 'th')
                                      ELSE situs_street_name
                                      END),
                          situs_street_type,
                          situs_street_post_dir),
                NULLIF(concat_ws(' ', 'UNIT', TRIM(situs_unit_number)), 'UNIT'),
                (SELECT CASE
                            WHEN H.situs_city = 'BC' THEN 'UNINCORPORATED'
                            WHEN H.situs_city = 'CK' THEN 'COCONUT CREEK'
                            WHEN H.situs_city = 'CS' THEN 'CORAL SPRINGS'
                            WHEN H.situs_city = 'CY' THEN 'COOPER CITY'
                            WHEN H.situs_city = 'DB' THEN 'DEERFIELD BEACH'
                            WHEN H.situs_city = 'DN' THEN 'DANIA BEACH'
                            WHEN H.situs_city = 'DV' THEN 'DAVIE'
                            WHEN H.situs_city = 'FL' THEN 'FORT LAUDERDALE'
                            WHEN H.situs_city = 'HA' THEN 'HALLANDALE BEACH'
                            WHEN H.situs_city = 'HB' THEN 'HILLSBORO BEACH'
                            WHEN H.situs_city = 'HW' THEN 'HOLLYWOOD'
                            WHEN H.situs_city = 'LH' THEN 'LAUDERHILL'
                            WHEN H.situs_city = 'LL' THEN 'LAUDERDALE LAKES'
                            WHEN H.situs_city = 'LP' THEN 'LIGHTHOUSE POINT'
                            WHEN H.situs_city = 'LS' THEN 'LAUD BY THE SEA'
                            WHEN H.situs_city = 'LZ' THEN 'LAZY LAKE'
                            WHEN H.situs_city = 'MG' THEN 'MARGATE'
                            WHEN H.situs_city = 'MM' THEN 'MIRAMAR'
                            WHEN H.situs_city = 'NL' THEN 'NORTH LAUDERDALE'
                            WHEN H.situs_city = 'OP' THEN 'OAKLAND PARK'
                            WHEN H.situs_city = 'PA' THEN 'PARKLAND'
                            WHEN H.situs_city = 'PB' THEN 'POMPANO BEACH'
                            WHEN H.situs_city = 'PI' THEN 'PEMBROKE PINES'
                            WHEN H.situs_city = 'PK' THEN 'PEMBROKE PARK'
                            WHEN H.situs_city = 'PL' THEN 'PLANTATION'
                            WHEN H.situs_city = 'SL' THEN 'SEA RANCH LAKES'
                            WHEN H.situs_city = 'SU' THEN 'SUNRISE'
                            WHEN H.situs_city = 'SW' THEN 'SOUTHWEST RANCHES'
                            WHEN H.situs_city = 'TM' THEN 'TAMARAC'
                            WHEN H.situs_city = 'WM' THEN 'WILTON MANORS'
                            WHEN H.situs_city = 'WP' THEN 'WEST PARK'
                            WHEN H.situs_city = 'WS' THEN 'WESTON'
                            ELSE H.situs_city
                            END),
                concat_ws(' ',
                          'FL',
                          (SELECT CASE
                                      WHEN length(situs_zip_code::VARCHAR) = 0 THEN NULL
                                      WHEN length(situs_zip_code::varchar) = 5 THEN situs_zip_code::varchar
                                      WHEN length(situs_zip_code::varchar) = 9
                                          THEN left(situs_zip_code::varchar, 5) END)
                    )
            ),
         concat_ws(' ', nullif(concat_ws(' - ', situs_street_number, situs_street_number_end), ''),
                   situs_street_direction, situs_street_name, situs_street_type, situs_street_post_dir),
         NULLIF(concat_ws(' ', 'UNIT', situs_unit_number), 'UNIT'),
         situs_unit_number,
         situs_street_name,
         situs_street_number,
         (SELECT CASE
                     WHEN situs_city = 'BC' THEN 'UNINCORPORATED'
                     WHEN situs_city = 'CK' THEN 'COCONUT CREEK'
                     WHEN situs_city = 'CS' THEN 'CORAL SPRINGS'
                     WHEN situs_city = 'CY' THEN 'COOPER CITY'
                     WHEN situs_city = 'DB' THEN 'DEERFIELD BEACH'
                     WHEN situs_city = 'DN' THEN 'DANIA BEACH'
                     WHEN situs_city = 'DV' THEN 'DAVIE'
                     WHEN situs_city = 'FL' THEN 'FORT LAUDERDALE'
                     WHEN situs_city = 'HA' THEN 'HALLANDALE BEACH'
                     WHEN situs_city = 'HB' THEN 'HILLSBORO BEACH'
                     WHEN situs_city = 'HW' THEN 'HOLLYWOOD'
                     WHEN situs_city = 'LH' THEN 'LAUDERHILL'
                     WHEN situs_city = 'LL' THEN 'LAUDERDALE LAKES'
                     WHEN situs_city = 'LP' THEN 'LIGHTHOUSE POINT'
                     WHEN situs_city = 'LS' THEN 'LAUD BY THE SEA'
                     WHEN situs_city = 'LZ' THEN 'LAZY LAKE'
                     WHEN situs_city = 'MG' THEN 'MARGATE'
                     WHEN situs_city = 'MM' THEN 'MIRAMAR'
                     WHEN situs_city = 'NL' THEN 'NORTH LAUDERDALE'
                     WHEN situs_city = 'OP' THEN 'OAKLAND PARK'
                     WHEN situs_city = 'PA' THEN 'PARKLAND'
                     WHEN situs_city = 'PB' THEN 'POMPANO BEACH'
                     WHEN situs_city = 'PI' THEN 'PEMBROKE PINES'
                     WHEN situs_city = 'PK' THEN 'PEMBROKE PARK'
                     WHEN situs_city = 'PL' THEN 'PLANTATION'
                     WHEN situs_city = 'SL' THEN 'SEA RANCH LAKES'
                     WHEN situs_city = 'SU' THEN 'SUNRISE'
                     WHEN situs_city = 'SW' THEN 'SOUTHWEST RANCHES'
                     WHEN situs_city = 'TM' THEN 'TAMARAC'
                     WHEN situs_city = 'WM' THEN 'WILTON MANORS'
                     WHEN situs_city = 'WP' THEN 'WEST PARK'
                     WHEN situs_city = 'WS' THEN 'WESTON' END),
         (SELECT CASE
                     WHEN situs_city = 'BC' THEN 'UNINCORPORATED'
                     WHEN situs_city = 'CK' THEN 'COCONUT CREEK'
                     WHEN situs_city = 'CS' THEN 'CORAL SPRINGS'
                     WHEN situs_city = 'CY' THEN 'COOPER CITY'
                     WHEN situs_city = 'DB' THEN 'DEERFIELD BEACH'
                     WHEN situs_city = 'DN' THEN 'DANIA BEACH'
                     WHEN situs_city = 'DV' THEN 'DAVIE'
                     WHEN situs_city = 'FL' THEN 'FORT LAUDERDALE'
                     WHEN situs_city = 'HA' THEN 'HALLANDALE BEACH'
                     WHEN situs_city = 'HB' THEN 'HILLSBORO BEACH'
                     WHEN situs_city = 'HW' THEN 'HOLLYWOOD'
                     WHEN situs_city = 'LH' THEN 'LAUDERHILL'
                     WHEN situs_city = 'LL' THEN 'LAUDERDALE LAKES'
                     WHEN situs_city = 'LP' THEN 'LIGHTHOUSE POINT'
                     WHEN situs_city = 'LS' THEN 'LAUD BY THE SEA'
                     WHEN situs_city = 'LZ' THEN 'LAZY LAKE'
                     WHEN situs_city = 'MG' THEN 'MARGATE'
                     WHEN situs_city = 'MM' THEN 'MIRAMAR'
                     WHEN situs_city = 'NL' THEN 'NORTH LAUDERDALE'
                     WHEN situs_city = 'OP' THEN 'OAKLAND PARK'
                     WHEN situs_city = 'PA' THEN 'PARKLAND'
                     WHEN situs_city = 'PB' THEN 'POMPANO BEACH'
                     WHEN situs_city = 'PI' THEN 'PEMBROKE PINES'
                     WHEN situs_city = 'PK' THEN 'PEMBROKE PARK'
                     WHEN situs_city = 'PL' THEN 'PLANTATION'
                     WHEN situs_city = 'SL' THEN 'SEA RANCH LAKES'
                     WHEN situs_city = 'SU' THEN 'SUNRISE'
                     WHEN situs_city = 'SW' THEN 'SOUTHWEST RANCHES'
                     WHEN situs_city = 'TM' THEN 'TAMARAC'
                     WHEN situs_city = 'WM' THEN 'WILTON MANORS'
                     WHEN situs_city = 'WP' THEN 'WEST PARK'
                     WHEN situs_city = 'WS' THEN 'WESTON' END),
         'FL',
         situs_zip_code,
         (SELECT CASE WHEN substring(folio_number, 7, 1) ~ E'^\\d+$' THEN FALSE ELSE TRUE END),
         (SELECT CASE
                     WHEN h.land_tag BETWEEN 1 AND 16 THEN TRUE
                     WHEN h.land_tag IN (24, 25, 26, 28, 62, 63, 64) THEN TRUE
                     WHEN h.land_tag BETWEEN 77 AND 86 THEN TRUE
                     ELSE FALSE
                     END),
         h.use_code,
         (SELECT CASE
                     WHEN actual_year_built = 0 THEN NULL
                     WHEN actual_year_built != 0 THEN actual_year_built END),
         bldg_adj_sq_footage,
         bldg_under_air_sq_footage,
         floor(baths),
         (SELECT CASE
                     WHEN floor(baths) NOTNULL AND floor(baths) != 0 THEN mod(baths, floor(baths))
                     WHEN floor(baths) = 0 THEN 1
                     END),
         beds,
         bldg_cclass::varchar,
         h.land_calc_prc_per_fact_unit_1,
         round(h.land_calc_fact_1 / 43560, 3),
         left(millage_code::varchar, 2)::int,
         h.use_code,
         h.land_tag,
         h.land_calc_fact_1
        )
FROM helper.bcpa_tax_roll_ib_july_2020_final h
WHERE h.folio_number = property.apn;


-- insert new sales
INSERT INTO sale (property_id, price, date, arms_length)
SELECT p.id,
       (SELECT CASE
                   WHEN sale_date_1 NOTNULL THEN (stamp_amount_1 /
                                                  (SELECT CASE
                                                              WHEN sale_date_1::date BETWEEN '1992-08-01' AND '2020-07-09'
                                                                  THEN 0.0070
                                                              WHEN sale_date_1::date BETWEEN '1991-06-01' AND '1992-07-31'
                                                                  THEN 0.0060
                                                              WHEN sale_date_1::date BETWEEN '1987-07-01' AND '1991-05-31'
                                                                  THEN 0.0055
                                                              WHEN sale_date_1::date BETWEEN '1985-07-01' AND '1987-06-30'
                                                                  THEN 0.0050
                                                              WHEN sale_date_1::date BETWEEN '1981-07-01' AND '1985-06-30'
                                                                  THEN 0.0045
                                                              WHEN sale_date_1::date BETWEEN '1979-10-01' AND '1981-06-30'
                                                                  THEN 0.0040
                                                              WHEN sale_date_1::date BETWEEN '1963-07-01' AND '1979-09-30'
                                                                  THEN 0.0030
                                                              WHEN sale_date_1::date BETWEEN '1957-07-01' AND '1963-06-30'
                                                                  THEN 0.0020
                                                              WHEN sale_date_1::date BETWEEN '1931-01-01' AND '1957-06-30'
                                                                  THEN 0.0010
                                                              ELSE 1
                                                              END))
                   END),
       sale_date_1::date,
       (SELECT CASE WHEN sale1_qual_code IN (1, 2, 4, 5, 6) AND sale_ver1 = 'Q' THEN TRUE ELSE FALSE END)
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE sale_date_1 NOTNULL;

INSERT INTO sale (property_id, price, date, arms_length)
SELECT p.id,
       (SELECT CASE
                   WHEN sale_date_2 NOTNULL THEN (stamp_amount_2 /
                                                  (SELECT CASE
                                                              WHEN sale_date_2::date BETWEEN '1992-08-01' AND '2020-07-09'
                                                                  THEN 0.0070
                                                              WHEN sale_date_2::date BETWEEN '1991-06-01' AND '1992-07-31'
                                                                  THEN 0.0060
                                                              WHEN sale_date_2::date BETWEEN '1987-07-01' AND '1991-05-31'
                                                                  THEN 0.0055
                                                              WHEN sale_date_2::date BETWEEN '1985-07-01' AND '1987-06-30'
                                                                  THEN 0.0050
                                                              WHEN sale_date_2::date BETWEEN '1981-07-01' AND '1985-06-30'
                                                                  THEN 0.0045
                                                              WHEN sale_date_2::date BETWEEN '1979-10-01' AND '1981-06-30'
                                                                  THEN 0.0040
                                                              WHEN sale_date_2::date BETWEEN '1963-07-01' AND '1979-09-30'
                                                                  THEN 0.0030
                                                              WHEN sale_date_2::date BETWEEN '1957-07-01' AND '1963-06-30'
                                                                  THEN 0.0020
                                                              WHEN sale_date_2::date BETWEEN '1931-01-01' AND '1957-06-30'
                                                                  THEN 0.0010
                                                              ELSE 1
                                                              END))
                   END),
       sale_date_2::date,
       (SELECT CASE WHEN sale2_qual_code IN (1, 2, 4, 5, 6) AND sale_ver2 = 'Q' THEN TRUE ELSE FALSE END)
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE sale_date_2 NOTNULL;

INSERT INTO sale (property_id, price, date, arms_length)
SELECT p.id,
       (SELECT CASE
                   WHEN sale_date_3 NOTNULL THEN (stamp_amount_3 /
                                                  (SELECT CASE
                                                              WHEN sale_date_3::date BETWEEN '1992-08-01' AND '2020-07-09'
                                                                  THEN 0.0070
                                                              WHEN sale_date_3::date BETWEEN '1991-06-01' AND '1992-07-31'
                                                                  THEN 0.0060
                                                              WHEN sale_date_3::date BETWEEN '1987-07-01' AND '1991-05-31'
                                                                  THEN 0.0055
                                                              WHEN sale_date_3::date BETWEEN '1985-07-01' AND '1987-06-30'
                                                                  THEN 0.0050
                                                              WHEN sale_date_3::date BETWEEN '1981-07-01' AND '1985-06-30'
                                                                  THEN 0.0045
                                                              WHEN sale_date_3::date BETWEEN '1979-10-01' AND '1981-06-30'
                                                                  THEN 0.0040
                                                              WHEN sale_date_3::date BETWEEN '1963-07-01' AND '1979-09-30'
                                                                  THEN 0.0030
                                                              WHEN sale_date_3::date BETWEEN '1957-07-01' AND '1963-06-30'
                                                                  THEN 0.0020
                                                              WHEN sale_date_3::date BETWEEN '1931-01-01' AND '1957-06-30'
                                                                  THEN 0.0010
                                                              ELSE 1
                                                              END))
                   END),
       sale_date_3::date,
       (SELECT CASE WHEN sale3_qual_code IN (1, 2, 4, 5, 6) AND sale_ver3 = 'Q' THEN TRUE ELSE FALSE END)
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE sale_date_3 NOTNULL;

INSERT INTO sale (property_id, price, date, arms_length)
SELECT p.id,
       (SELECT CASE
                   WHEN sale_date_4 NOTNULL THEN (stamp_amount_4 /
                                                  (SELECT CASE
                                                              WHEN sale_date_4::date BETWEEN '1992-08-01' AND '2020-07-09'
                                                                  THEN 0.0070
                                                              WHEN sale_date_4::date BETWEEN '1991-06-01' AND '1992-07-31'
                                                                  THEN 0.0060
                                                              WHEN sale_date_4::date BETWEEN '1987-07-01' AND '1991-05-31'
                                                                  THEN 0.0055
                                                              WHEN sale_date_4::date BETWEEN '1985-07-01' AND '1987-06-30'
                                                                  THEN 0.0050
                                                              WHEN sale_date_4::date BETWEEN '1981-07-01' AND '1985-06-30'
                                                                  THEN 0.0045
                                                              WHEN sale_date_4::date BETWEEN '1979-10-01' AND '1981-06-30'
                                                                  THEN 0.0040
                                                              WHEN sale_date_4::date BETWEEN '1963-07-01' AND '1979-09-30'
                                                                  THEN 0.0030
                                                              WHEN sale_date_4::date BETWEEN '1957-07-01' AND '1963-06-30'
                                                                  THEN 0.0020
                                                              WHEN sale_date_4::date BETWEEN '1931-01-01' AND '1957-06-30'
                                                                  THEN 0.0010
                                                              ELSE 1
                                                              END))
                   END),
       sale_date_4::date,
       (SELECT CASE WHEN sale4_qual_code::int IN (1, 2, 4, 5, 6) AND sale_ver4 = 'Q' THEN TRUE ELSE FALSE END)
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE sale_date_4 NOTNULL;

INSERT INTO sale (property_id, price, date, arms_length)
SELECT p.id,
       (SELECT CASE
                   WHEN sale_date_5 NOTNULL THEN (stamp_amount_5 /
                                                  (SELECT CASE
                                                              WHEN sale_date_5::date BETWEEN '1992-08-01' AND '2020-07-09'
                                                                  THEN 0.0070
                                                              WHEN sale_date_5::date BETWEEN '1991-06-01' AND '1992-07-31'
                                                                  THEN 0.0060
                                                              WHEN sale_date_5::date BETWEEN '1987-07-01' AND '1991-05-31'
                                                                  THEN 0.0055
                                                              WHEN sale_date_5::date BETWEEN '1985-07-01' AND '1987-06-30'
                                                                  THEN 0.0050
                                                              WHEN sale_date_5::date BETWEEN '1981-07-01' AND '1985-06-30'
                                                                  THEN 0.0045
                                                              WHEN sale_date_5::date BETWEEN '1979-10-01' AND '1981-06-30'
                                                                  THEN 0.0040
                                                              WHEN sale_date_5::date BETWEEN '1963-07-01' AND '1979-09-30'
                                                                  THEN 0.0030
                                                              WHEN sale_date_5::date BETWEEN '1957-07-01' AND '1963-06-30'
                                                                  THEN 0.0020
                                                              WHEN sale_date_5::date BETWEEN '1931-01-01' AND '1957-06-30'
                                                                  THEN 0.0010
                                                              ELSE 1
                                                              END))
                   END),
       sale_date_5::date,
       (SELECT CASE WHEN sale5_qual_code::int IN (1, 2, 4, 5, 6) AND sale_ver5 = 'Q' THEN TRUE ELSE FALSE END)
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE sale_date_5 NOTNULL;

-- remove duplicates from sales
DELETE
FROM sale t1 USING sale t2
WHERE t1.property_id = t2.property_id
  AND t1.price = t2.price
  AND t1.date = t2.date
  AND t1.CTID > t2.CTID;

-- insert assessments
INSERT INTO assessment_files (assessment_date_id, file_name)
VALUES (8, 'BCPA_TAX_ROLL_IB_JULY_2020_FINAL.csv');

INSERT INTO assessment(assessment_id, property_id, value, assessment_type)
SELECT 8, p.id, new_soh_value, 'tent'
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn;


-- insert owners
INSERT INTO owner (data_source, property_id, created_on, first_name, second_owner_first_name, owner_address_1,
                   owner_address_2, owner_city, owner_zip, owner_state)
SELECT 'assessment',
       p.id,
       '2020-07-08',
       h.name_line_1,
       h.name_line_2,
       h.address_line_1,
       h.address_line_2,
       h.city,
       (SELECT CASE WHEN h.zip ~ E'^\\d+$' THEN h.zip::integer END),
       h.state
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn;

-- update property class
UPDATE property
SET property_class_type = use_type
FROM helper.bcpa_tax_roll_ib_july_2020_final h
WHERE h.folio_number = property.apn;


-- update lot_size
UPDATE property
SET lot_size = lot_size::float / 43560
WHERE county = 'broward'
  AND lot_size NOTNULL;

-- update watercategory

UPDATE property
SET water_category = CASE
                         WHEN land_tag IN (1, 2, 62) THEN 1
                         WHEN land_tag IN (03,
                                           05,
                                           07,
                                           24,
                                           63,
                                           64) THEN 2
                         WHEN land_tag IN (04,
                                           09,
                                           10,
                                           78,
                                           79) THEN 3
                         WHEN land_tag IN (06,
                                           08,
                                           11,
                                           25,
                                           77,
                                           80) THEN 4
                         WHEN land_tag IN (12,
                                           13,
                                           14,
                                           15,
                                           26,
                                           81,
                                           82,
                                           83,
                                           84,
                                           86) THEN 5
                         WHEN land_tag IN (16,
                                           28,
                                           85) THEN 6 END
WHERE county = 'broward';

-- updating assessment table

UPDATE assessment
SET assessment_value = value
WHERE assessment_id = 8;

UPDATE assessment
SET value = just_land_value + just_building_value
FROM helper.bcpa_tax_roll_ib_july_2020_final h
         JOIN property p ON h.folio_number = p.apn
WHERE assessment_id = 8
  AND property_id = p.id;

-- update sale dates ....remove those dates from the future
UPDATE sale
SET date = date - INTERVAL '100 years'
WHERE date > '2021-01-01';

-- update is_residetial...that is to say is_whitelisted for broward...
-- refer to WHITELISTED_PROPERTY_CLASS_CODES for reference
UPDATE property p
SET is_residential = TRUE
WHERE p.county = 'broward'
  AND (
        (p.property_class = 1 AND p.property_class_type = 1)
        OR (p.property_class = 1 AND p.property_class_type = 2)
        OR (p.property_class = 1 AND p.property_class_type = 4)
        OR (p.property_class = 1 AND p.property_class_type = 5)
        OR (p.property_class = 1 AND p.property_class_type = 6)
        OR (p.property_class = 8 AND p.property_class_type = 1)
        OR (p.property_class = 8 AND p.property_class_type = 2)
        OR (p.property_class = 8 AND p.property_class_type = 3)
        OR (p.property_class = 8 AND p.property_class_type = 4)
        OR (p.property_class = 0 AND p.property_class_type = 1)
        OR (p.property_class = 0 AND p.property_class_type = 3)
        OR (p.property_class = 0 AND p.property_class_type = 4)
        OR (p.property_class = 0 AND p.property_class_type IS NULL)
    );

--update address
UPDATE property
SET address_line_2 = replace(address_line_2, '#', ''),
    address = replace(address, '#', '')
WHERE address_line_2 ILIKE '%#%'
  AND county = 'broward';

--update lot size and price per sqft
UPDATE property
SET (lot_size, price_per_sqft) = (
                                  round(h.land_calc_fact_1 / 43560, 3),
                                  h.land_calc_prc_per_fact_unit_1
    )
FROM helper.bcpa_tax_roll_ib_july_2020_final h
WHERE property.apn = h.folio_number
  AND property.county = 'broward';


-- update legal
UPDATE property
SET legal = legal_line_1
FROM helper.bcpa_tax_roll_ib_july_2020_final
WHERE property.apn = folio_number
  AND property.county = 'broward';

-- update subdivision
UPDATE property
SET subdivision= h.legal_line_1
FROM helper.bcpa_tax_roll_ib_july_2020_final h
WHERE property.apn = h.folio_number
      and property.county = 'broward';

-- update effective_age
UPDATE property
SET effective_age = bldg_year_built
FROM helper.bcpa_tax_roll_ib_july_2020_final
WHERE county = 'broward'
  AND apn = folio_number;

