#!/bin/bash
set -e

echo "Usage [pokec.db] [path-to-neo4j] [path-to-benchmark]"
NEO=${2-databases}
DB=$NEO/data/databases/${1-pokec.db}
BENCHMARK=${3-`pwd`}
TMP=~/Documents/nosql-tests
DOWNLOADS=$TMP/downloads

PROFILES_IN=$DOWNLOADS/soc-pokec-profiles.txt.gz
PROFILES_OUT=$DOWNLOADS/soc-pokec-profiles-neo4j.txt.gz
PROFILES_HEADER=$DOWNLOADS/profiles_header.txt

RELATIONS_IN=$DOWNLOADS/soc-pokec-relationships.txt.gz
RELATIONS_OUT=$DOWNLOADS/soc-pokec-relationships-neo4j.txt.gz
RELATIONS_HEADER=$DOWNLOADS/relations_header.txt

echo "DATABASE: $DB"
echo "NEO4J DIRECTORY: $NEO"
echo "BENCHMARK DIRECTORY: $BENCHMARK"
echo "DOWNLOAD DIRECTORY: $DOWNLOADS"

#$BENCHMARK/downloadData.sh


if [ ! -f $PROFILES_OUT ]; then
  echo "Removing NULL values"
  gzip -dc $PROFILES_IN | sed -e 's/null//g' -e 's~^~P~' | sort -k1 --parallel=10 -S 5G | gzip > $PROFILES_OUT
fi

if [ ! -f $RELATIONS_OUT ]; then
  echo "Converting RELATIONS"
  gzip -dc $RELATIONS_IN | awk -F"\t" '{print "P" $1 "\tP" $2}' | gzip > $RELATIONS_OUT
fi

echo "_key:ID	public:INT	completion_percentage	gender:INT	region	last_login	registration	AGE:INT	" > $PROFILES_HEADER

echo ':START_ID	:END_ID' > $RELATIONS_HEADER

export IDTYPE=string #actual
rm -rf $DB

echo "Starting IMPORT"
$NEO/bin/neo4j-import --into $DB --id-type $IDTYPE --delimiter TAB --quote Ö  --nodes:PROFILES $PROFILES_HEADER,$PROFILES_OUT --relationships:RELATIONS $RELATIONS_HEADER,$RELATIONS_OUT

echo "Creating INDEX"
$NEO/bin/neo4j start

sleep 20

JAVA_OPTS="-Xmx2G -Xmn512m" $NEO/bin/neo4j-shell -host localhost -port 1337 -c 'create index on :PROFILES(_key);'
#JAVA_OPTS="-Xmx2G -Xmn512m" $NEO/bin/neo4j-admin -host localhost -port 1337 -c 'create index on :PROFILES(_key);'
echo "Wait for the index to be populated"
sleep 60

#$NEO/bin/neo4j stop

