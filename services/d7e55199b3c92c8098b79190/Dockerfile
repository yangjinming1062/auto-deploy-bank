# Stage 1: Build the plugin
FROM gradle:7.4.2-jdk17 AS builder

WORKDIR /home/gradle/project

# Copy build configuration files
COPY build.gradle gradle.properties settings.gradle ./

# Copy source files
COPY src ./src

# Build the plugin
RUN gradle packageDistribution -x test --no-daemon

# Stage 2: Create the Elasticsearch plugin image
FROM docker.elastic.co/elasticsearch/elasticsearch:8.5.0

# Copy the built plugin JAR for security scanning
COPY --from=builder /home/gradle/project/build/libs/ingest-opennlp-8.5.0.1-SNAPSHOT.jar /app/target.jar

# Copy the built plugin distribution ZIP from builder stage
COPY --from=builder /home/gradle/project/build/distribution/elasticsearch-ingest-opennlp.zip /tmp/

# Download NER model files for the plugin (follow redirects)
RUN mkdir -p /usr/share/elasticsearch/config/ingest-opennlp && \
    curl -sL -o /usr/share/elasticsearch/config/ingest-opennlp/en-ner-persons.bin \
        http://opennlp.sourceforge.net/models-1.5/en-ner-person.bin && \
    curl -sL -o /usr/share/elasticsearch/config/ingest-opennlp/en-ner-locations.bin \
        http://opennlp.sourceforge.net/models-1.5/en-ner-location.bin && \
    curl -sL -o /usr/share/elasticsearch/config/ingest-opennlp/en-ner-dates.bin \
        http://opennlp.sourceforge.net/models-1.5/en-ner-date.bin && \
    ls -la /usr/share/elasticsearch/config/ingest-opennlp/

# Install the plugin
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install --batch file:///tmp/elasticsearch-ingest-opennlp.zip || true

# Set environment variables for the plugin
ENV ES_SETTING_INGEST_OPENNLP_MODEL_FILE_NAMES=en-ner-persons.bin
ENV ES_SETTING_INGEST_OPENNLP_MODEL_FILE_LOCATIONS=en-ner-locations.bin
ENV ES_SETTING_INGEST_OPENNLP_MODEL_FILE_DATES=en-ner-dates.bin

# Set discovery type to single-node for development
ENV discovery.type=single-node
ENV xpack.security.enabled=false

# Expose Elasticsearch port
EXPOSE 9200

# Run Elasticsearch in foreground
CMD ["/usr/share/elasticsearch/bin/elasticsearch"]