--update miami sales

UPDATE sale
SET arms_length = (
    CASE
        WHEN "Sale Date 1" != '' AND date = "Sale Date 1"::date AND price = "Sale Amt 1"::integer AND
             "Sale Qual 1" = 'Q' AND
             "Sale Type 1" IN ('01', '02', '04', '05', '06') THEN TRUE
        WHEN "Sale Date 2" != '' AND date = "Sale Date 2"::date AND price = "Sale Amt 2"::integer AND
             "Sale Qual 2" = 'Q' AND
             "Sale Type 2" IN ('01', '02', '04', '05', '06') THEN TRUE
        WHEN "Sale Date 3" != '' AND date = "Sale Date 3"::date AND price = "Sale Amt 3"::integer AND
             "Sale Qual 3" = 'Q' AND
             "Sale Type 3" IN ('01', '02', '04', '05', '06') THEN TRUE
        ELSE FALSE
        END
    )
FROM helper.miamidade_property_2020
         JOIN property p ON miamidade_property_2020."Folio" = p.apn
WHERE property_id = p.id;



-- update miami address

-- update address line 1 when it is null
UPDATE property
SET address_line_1 = concat(number, street)
WHERE county = 'miamidade'
  AND address_line_1 ISNULL
  AND (number IS NOT NULL OR street IS NOT NULL);


UPDATE property
SET address_line_1 = "Property Address"
FROM helper.miamidade_property_2020
WHERE apn = "Folio"
  AND county = 'miamidade'
  AND address_line_1 NOTNULL
  AND number ISNULL;


UPDATE property
SET address_unit = "Legal2"
FROM helper.miamidade_property_2020
WHERE county = 'miamidade'
  AND address_unit = 'UNIT'
  AND address LIKE '%' || address_unit || '%'
  AND apn = "Folio";

--updating 800 properties. Might be insignificant.
UPDATE property
SET address_line_1 = "Property Address",
    address_unit   = "Legal2"
FROM helper.miamidade_property_2020
WHERE address_line_1 IS NULL
  AND property.county = 'miamidade'
  AND apn = "Folio"
  AND "Property Address" != '';

-- remove multiple space in address unit
UPDATE property
SET address_unit = trim(regexp_replace(address_unit, '\s+', ' ', 'g'))
WHERE county = 'miamidade'
  AND address_unit NOTNULL;

-- remove multiple space in address line 1 unit
UPDATE property
SET address_line_1 = trim(regexp_replace(address_line_1, '\s+', ' ', 'g'))
WHERE county = 'miamidade'
  AND address_line_1 NOTNULL
  AND regexp_replace(address_line_1, '^.* ', '') = regexp_replace(address_unit, '^.* ', '');

-- update address line 1....2k updated
WITH foo AS (
    SELECT apn,
           number,
           street,
           address_line_1,
           address_line_2,
           address_unit,
           address,
           town,
           zip,
           state
    FROM property
    WHERE county = 'miamidade'
      AND address_unit NOTNULL
      AND address_line_1 NOTNULL
      AND address_line_2 ISNULL
)
-- SELECT apn, address_line_1, address_unit, concat_ws(', ', trim(replace(address_line_1, replace(address_unit, 'UNIT ', ''),'')), address_unit) as addr
UPDATE property p
SET address_line_1 = concat_ws(', ', trim(replace(p.address_line_1, replace(p.address_unit, 'UNIT ', ''), '')),
                               p.address_unit)
FROM foo
WHERE regexp_replace(p.address_line_1, '^.* ', '') = regexp_replace(p.address_unit, '^.* ', '')
  AND foo.apn = p.apn;


UPDATE property
SET address =
        concat_ws(' ', concat_ws(', ', address_line_1, address_line_2, town, state), zip)
WHERE address_line_1 IS NOT NULL
  AND county = 'miamidade';

-- update legal
UPDATE property
SET legal = "Legal1"
FROM helper.miamidade_property_2020
WHERE property.apn = "Folio"
  AND property.county = 'miamidade';


-- update is_residential
-- refer to WHITELISTED_PROPERTY_CLASS_CODES for reference
UPDATE property p
SET is_residential = TRUE
WHERE p.property_class IN (1, 4, 5, 7, 10, 17, 23, 40, 65, 66, 80, 81, 89,
                           101, 102, 104, 105, 405, 407, 410, 802, 803)
  AND county = 'miamidade';


-- update subdivision
UPDATE property
SET subdivision = legal
WHERE property.county = 'miamidade';


UPDATE property
SET effective_age = "EffectiveYearBuilt"
FROM helper.miamidade_property_2020
WHERE county = 'miamidade'
  AND apn = "Folio";


UPDATE property
SET age = NULL
WHERE age = 0
  AND county IN ('broward', 'miamidade');

UPDATE property
SET effective_age = NULL
WHERE effective_age = 0
  AND county IN ('broward', 'miamidade');

