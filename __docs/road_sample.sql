CREATE OR REPLACE FUNCTION temp.ST_ForceClosed_road_obs_2e4012c0523d4762b9c81aeecac116dd(geom geometry)
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
            SELECT temp.ST_ForceClosed_road_obs_2e4012c0523d4762b9c81aeecac116dd(gd.geom) AS closed_geom
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
CREATE OR REPLACE FUNCTION temp.ISOVIST_roads_crop_2e4012c0523d4762b9c81aeecac116dd(IN center geometry,
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
--                  excluded_rays_limit AS (
--                      SELECT min(id), max(id)
--                      FROM rays_all
--                      WHERE st_length(ST_Intersection(geom,
--                                                      prop_gis)) >= 0.00001
--                  ),
             rays AS (
                 SELECT id, geom
                 FROM rays_all
                 WHERE st_length(ST_Intersection(geom,
                                                 prop_gis)) < 0.00001
             ),
             intersections AS (
                 SELECT r.id,
                        (ST_Dump(ST_Intersection(ST_Boundary(b.geom), r.geom))).geom AS point
                 FROM rays r
                          LEFT JOIN
                      temp.near_road_props_2e4012c0523d4762b9c81aeecac116dd b
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
                 SELECT ST_MakePolygon(temp.ST_ForceClosed_road_obs_2e4012c0523d4762b9c81aeecac116dd(
                         ST_MakeLine(geom))) AS geom
                 FROM intersection_closest
             ),
             isovist_buildings AS (
                 SELECT b.property_id AS p_id, b.geom AS geom
                 FROM isovist_0 i,
                      temp.near_road_props_2e4012c0523d4762b9c81aeecac116dd b
                 WHERE st_dwithin(b.geom, i.geom,
                                  0.00000001)
             )
        SELECT b.p_id, b.geom
        FROM isovist_buildings b

        UNION
        SELECT *
        FROM rays;
END;
$$ LANGUAGE plpgsql IMMUTABLE;


SELECT *
FROM temp.ISOVIST_roads_crop_2e4012c0523d4762b9c81aeecac116dd(
        (SELECT ST_GeomFromEWKB('\x0101000020E6100000881A51EC060954C04FFFAA7C35323A40'::bytea)), ST_GeomFromEWKB(
                '\x0102000020e6100000130000001cf1bff0250954c026231dd434323a40f9179c1c190954c02c84301235323a40c0acf5ea080954c0a95d5d5f35323a40671f7585080954c0d3dc0a6135323a408f441e77000954c056174bec35323a40dc2340f2f30854c0e4cbfa8337323a401fe516a9e60854c01969f34938323a409cf7a4b8cf0854c05ac8128c39323a4000ab2347ba0854c07db262b83a323a409efd929eb30854c07104a9143b323a40d13a4fe1ad0854c041dc30653b323a4057aab0bea60854c005aadac93b323a40d19332a9a10854c0db8651103c323a4010a7ddf98f0854c0e7a49cd43c323a405ca560327a0854c09372f7393e323a4023cd6960750854c0872062de3e323a4018dd30c0740854c0a49531f43e323a402412e04f680854c0eb9d1be43f323a40261e5036650854c03ef89a2f40323a40'::bytea),
        100);
