CREATE OR REPLACE FUNCTION temp.ST_ForceClosed_obs7d0cd982996643ccab6ff4b90da1e577(geom geometry)
    RETURNS geometry AS
$BODY$
BEGIN
    IF ST_IsClosed(geom) THEN
        RETURN geom;
    ELSIF GeometryType(geom) = 'LINESTRING' THEN
        SELECT ST_AddPoint(geom, ST_StartPoint(geom)) INTO geom;
    ELSIF GeometryType(geom) ~ '(MULTI|COLLECTION)' THEN
        -- Recursively deconstruct parts
        WITH parts AS (
            SELECT temp.ST_ForceClosed_obs7d0cd982996643ccab6ff4b90da1e577(gd.geom) AS closed_geom
            FROM ST_Dump(geom) AS gd
        ) -- Reconstitute parts
        SELECT ST_Collect(closed_geom)
        INTO geom
        FROM parts;
    END IF;
    IF NOT ST_IsClosed(geom) THEN
        RAISE EXCEPTION 'Could not close geometry';
    END IF;
    RETURN geom;
END;
$BODY$ LANGUAGE plpgsql IMMUTABLE
                        COST 42;

CREATE OR REPLACE FUNCTION temp.ISOVIST_buildings_crop7d0cd982996643ccab6ff4b90da1e577(IN center geometry,
                                                                                       IN prop_gis geometry,
                                                                                       IN radius numeric DEFAULT 100,
                                                                                       IN rays integer DEFAULT 36,
                                                                                       IN heading integer DEFAULT -999,
                                                                                       IN fov integer DEFAULT 360)
    RETURNS table
            (
                p_id integer,
                gm   geometry
            )
AS
$$
DECLARE
    arc     numeric;
    angle_0 numeric;
BEGIN
    arc := fov::numeric / rays::numeric;
    IF fov = 360 THEN
        angle_0 := 0;
    ELSE
        angle_0 := heading - 0.5 * fov;
    END IF;
    RETURN QUERY
        WITH rays_all AS (
            SELECT t.n   AS id,

                   ST_MakeLine(
                           center,
                           ST_Project(
                                   center::geography,
                                   radius + 1,
                                   RADIANS(angle_0 + t.n::numeric * arc)
                               )::geometry
                       ) AS geom
            FROM GENERATE_SERIES(0, rays) AS t(n)
        ),
             excluded_rays_limit AS (
                 SELECT MIN(id), MAX(id)
                 FROM rays_all
                 WHERE st_length(ST_Intersection(geom,
                                                 prop_gis)) >= 0.00001
             ),
             rays AS (
                 SELECT id, geom
                 FROM rays_all
                 WHERE id <
                       MOD(36 + MOD((SELECT min FROM excluded_rays_limit) - 4, 36), 36)
                    OR id >
                       MOD(36 + MOD((SELECT max FROM excluded_rays_limit) + 4, 36), 36)
             ),
             intersections AS (
                 SELECT r.id,
                        (ST_Dump(ST_Intersection(ST_Boundary(b.geom), r.geom))).geom AS point
                 FROM rays r
                          LEFT JOIN
                      temp.within_100m_props_7d0cd982996643ccab6ff4b90da1e577 b
                      ON
                          ST_Intersects(b.geom, r.geom)
             ),
             intersections_distances AS (
                 SELECT id,
                        point                                                         AS geom,
                        ROW_NUMBER() OVER (PARTITION BY id ORDER BY center <-> point) AS ranking
                 FROM intersections
             ),
             intersection_closest AS (
                 SELECT -1                                                      AS id,
                        CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
                 UNION ALL
                 (SELECT id,
                         geom
                  FROM intersections_distances
                  WHERE ranking = 1
                  ORDER BY id)
                 UNION ALL
                 SELECT 999999                                                  AS id,
                        CASE WHEN fov = 360 THEN NULL::geometry ELSE center END AS geom
             ),
             isovist_0 AS (
                 SELECT ST_MakePolygon(
                                temp.ST_ForceClosed_obs7d0cd982996643ccab6ff4b90da1e577(ST_MakeLine(geom))) AS geom
                 FROM intersection_closest
             ),
             isovist_buildings AS (
                 SELECT b.property_id AS p_id, b.geom AS geom
                 FROM isovist_0 i,
                      temp.within_100m_props_7d0cd982996643ccab6ff4b90da1e577 b
                 WHERE st_dwithin(b.geom, i.geom,
                                  0.00000001)
             )
        SELECT b.p_id, b.geom
        FROM isovist_buildings b

        UNION
        SELECT *
        FROM rays
    ;
END;
$$ LANGUAGE plpgsql IMMUTABLE;



SELECT *
FROM temp.ISOVIST_buildings_crop7d0cd982996643ccab6ff4b90da1e577(
        (SELECT ST_GeomFromEWKB('\x0101000020E6100000E97D0CB1166852C04A1B9AAA40674440'::bytea)), ST_GeomFromEWKB(
                '\x0103000020E6100000010000002F000000BC32646FD76752C008DAFE3A3D6744404B35BE22016852C0E21B06FC27674440BC130B38046852C088AF1B002B674440F6B2723F046852C0A01338082B674440E0A92647046852C0106ADC0F2B6744405DD3DB4E046852C011B60C172B6744401C90DE56046852C06ADAC81D2B67444070B7085F046852C00EFF0D242B67444061373267046852C09427172A2B674440C32EAB6F046852C0E43B702F2B674440A2792378046852C034438F342B6744409382C280046852C0D53DFD382B674440CD246289046852C03A33313D2B6744409C312992046852C0E628EE402B6744405DF7169B046852C00201FC432B674440835B05A4046852C0BEE4CD462B67444067BE1BAD046852C0ADB2F0482B6744404F060AB6046852C0CB93D64A2B674440105220BF046852C0FC6F0B4C2B6744402AFE5DC8046852C0A92ACD4C2B674440777375D1046852C0F90B164D2B67444087D58CDA046852C016DBEA4C2B6744407529A4E3046852C0E2A8494C2B6744405E74BBEC046852C04086304B2B674440D3F1D3F5046852C02B59A3492B674440422EC6FE046852C0F530A1472B674440D72DDF07056852C0F00CEC442B6744403620AB10056852C026F9FC412B67444058379D19056852C0E0DD963E2B674440ED784322056852C050D9803A2B6744401913E92A056852C0A9D82E362B674440EAE48F33056852C071DE66312B6744409855E83B056852C068EBEE2B2B67444071AA4244056852C0D10B3B262B6744407478754C056852C0512912202B674440F3965A54056852C0E16B71192B67444017ED405C056852C0E2B45A122B674440EB680064056852C0FD07090B2B674440926536FA0E6852C008BC68D024674440E5181483166852C0BE21D8FA3F6744404A689C791A6852C0A1F6B1214F6744409A43C27DF66752C0DD5DFBBC5F6744402CBB018AF56752C0BA10A8797067444083C724C7F06752C0581BF0B2726744406B8E15B5DF6752C0FB4EB88181674440E504B622DE6752C0CEB46CE782674440BC32646FD76752C008DAFE3A3D674440'::bytea),
        100);
