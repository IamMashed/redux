
# download file
wget ftp://sdrftp03.dor.state.fl.us/Map%20Data/2019%20PIN%20Data%20Distribution/dade_2019pin.zip

# unzip
unzip dade_2019pin.zip

# load shapes to postgis
shp2pgsql -s 4152:4326 -g geom_4326 "dade_2019pin" helper.dade_2019pin | psql -h beta-global-cma-database.cpomb8cyzs42.us-east-2.rds.amazonaws.com -d betaglobalcma -U postgres

shp2pgsql -g geom "Nassau_2017_Tax_Parcels_SHP_1808" data_source.nassau_gis | psql -h localhost -d test_globalcma -U postgres

# refer to update_gis.sql for next steps