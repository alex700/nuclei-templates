#!/bin/sh
set -eu
cat > /usr/local/tomcat/lib/roller-custom.properties <<EOF
installation.type=auto
mediafiles.storage.dir=/var/lib/roller/mediafiles
search.index.dir=/var/lib/roller/searchindex
database.configurationType=jdbc
database.jdbc.driverClass=org.postgresql.Driver
database.jdbc.connectionURL=jdbc:postgresql://${DB_HOST}:5432/rollerdb
database.jdbc.username=roller
database.jdbc.password=rollerlab
mail.configurationType=properties
mail.host=localhost
EOF
exec /usr/local/tomcat/bin/catalina.sh run
