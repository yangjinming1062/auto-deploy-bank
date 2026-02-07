#!/bin/bash
# Entrypoint script to copy JAR to volume mount point and start Elasticsearch

# Create the target.jar file by copying from the backup
mkdir -p /data
cp ${ES_HOME}/plugins/mongodb-river/lib/elasticsearch-river-mongodb-2.0.12-SNAPSHOT.jar.bak /data/target.jar

# Execute Elasticsearch
exec ${ES_HOME}/bin/elasticsearch