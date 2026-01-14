#
# The contents of this file are subject to the license and copyright
# detailed in the LICENSE and NOTICE files at the root of the source
# tree and available online at
#
# http://www.dspace.org/license/
#

# To build use root as context for (easier) access to solr cfgs
# docker build --build-arg SOLR_VERSION=9.8 -f ./dspace/src/main/docker/dspace-solr/Dockerfile .
# This will be published as dspace/dspace-solr:$DSPACE_VERSION

ARG SOLR_VERSION=9.8

# NOTE: Cannot use the "-slim" image because it doesn't include the extra modules needed for DSpace (e.g. icu4j)
FROM docker.io/solr:${SOLR_VERSION}

# Customize SOLR_OPTS to enable "<lib>" tags in solrconfig.xml files
# Configsets must be in /var/solr/data/configsets/ for Solr to find them
ENV SOLR_OPTS="-Dsolr.config.lib.enabled=true"

USER root

# Create configset directories in the location Solr expects
RUN mkdir -p /var/solr/data/configsets/authority/conf && \
    mkdir -p /var/solr/data/configsets/oai/conf && \
    mkdir -p /var/solr/data/configsets/search/conf && \
    mkdir -p /var/solr/data/configsets/statistics/conf && \
    mkdir -p /var/solr/data/configsets/qaevent/conf && \
    mkdir -p /var/solr/data/configsets/suggestion/conf

# NOTE: "solrconfigs" MUST be passed in by docker-compose via "additional_contexts"
# OR via "docker build --build-context solrconfigs=[path-to-dspace/solr]"
COPY --from=solrconfigs authority/conf/* /var/solr/data/configsets/authority/conf/
COPY --from=solrconfigs oai/conf/* /var/solr/data/configsets/oai/conf/
COPY --from=solrconfigs search/conf/* /var/solr/data/configsets/search/conf/
COPY --from=solrconfigs statistics/conf/* /var/solr/data/configsets/statistics/conf/
COPY --from=solrconfigs qaevent/conf/* /var/solr/data/configsets/qaevent/conf/
COPY --from=solrconfigs suggestion/conf/* /var/solr/data/configsets/suggestion/conf/

# Ensure solr user can write to data directory for core creation
RUN chown -R solr:solr /var/solr/data && \
    chmod 755 /var/solr/data

USER solr
