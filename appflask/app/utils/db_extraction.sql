-- 1. create table
-- 2. extract table

-- from pycharm
-- /usr/bin/pg_dump --dbname=betaglobalcma --schema=public --table=public.\"suffolk_gis\" --file=/home/<user_name>/live_globalcma-suffolk-gis-2021_02_09_12_27_33-dump.sql --username=postgres --host=localhost --port=34295

-- create nassau_property table
create table nassau_property as
select * from public.property
where county = 'nassau';

-- create nassau_owner table
create table nassau_owner as
    (
        select o.* from owner o
    inner join property p on p.id = o.property_id
    where county='nassau'
    order by property_id
        );

-- create nassau_gis table
create table nassau_gis as (
    select * from property_gis
    where county='nassau'
);


-- create suffolk_property table
create table suffolk_property as
(select * from public.property
where county = 'suffolk');

-- create suffolk_owner table
create table suffolk_owner as
    (
        select o.* from owner o
    inner join property p on p.id = o.property_id
    where county='suffolk'
    order by property_id
        );

-- create suffolk_gis table
create table suffolk_gis as (
    select * from property_gis
    where county='suffolk'
);
