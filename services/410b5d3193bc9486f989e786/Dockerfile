## Docker GROBID image
## GROBID is a machine learning library for extracting, parsing and re-structuring
## raw PDF documents into structured XML/TEI encoded documents.

## Build:
## docker build -t grobid/grobid:latest .

## Run:
## docker run -t --rm -p 40381:8070 -p 8071:8071 grobid/grobid:latest

## -------------------
## Build stage
## -------------------
FROM eclipse-temurin:21-jdk AS builder

USER root

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y --no-install-recommends install unzip git

WORKDIR /opt/grobid-source

# Copy Gradle wrapper and configuration
COPY gradle/ ./gradle/
COPY gradlew ./
COPY gradle.properties ./
COPY build.gradle ./
COPY settings.gradle ./

# Copy source code
COPY grobid-home/ ./grobid-home/
COPY grobid-core/ ./grobid-core/
COPY grobid-service/ ./grobid-service/
COPY grobid-trainer/ ./grobid-trainer/

# Clean unused native libraries before packaging (keep only Linux x86_64)
RUN rm -rf grobid-home/pdf2xml && \
    rm -rf grobid-home/pdfalto/lin-32 && \
    rm -rf grobid-home/pdfalto/mac-64 && \
    rm -rf grobid-home/pdfalto/mac_arm-64 && \
    rm -rf grobid-home/pdfalto/win-* && \
    rm -rf grobid-home/lib/lin-32 && \
    rm -rf grobid-home/lib/win-* && \
    rm -rf grobid-home/lib/mac-64 && \
    rm -rf grobid-home/lib/mac_arm-64

# Clean Deep Learning models (keeping only CRF models)
RUN rm -rf grobid-home/models/*-BidLSTM_CRF* && \
    rm -rf grobid-home/models/*-BidLSTM_ChainCRF* && \
    rm -rf grobid-home/models/*gru* && \
    rm -rf grobid-home/models/*bert*

# Set Java library path for native libraries
ENV GROBID_SERVICE_OPTS="-Djava.library.path=grobid-home/lib/lin-64:grobid-home/lib/lin-64/jep"

# Build the project
RUN ./gradlew clean assemble --no-daemon --info --stacktrace

# Extract distributions
WORKDIR /opt/grobid
RUN unzip -o /opt/grobid-source/grobid-service/build/distributions/grobid-service-*.zip && \
    mv grobid-service* grobid-service && \
    unzip -o /opt/grobid-source/grobid-home/build/distributions/grobid-home-*.zip && \
    chmod -R 755 /opt/grobid/grobid-home/pdfalto && \
    rm -rf grobid-source

# -------------------
## Runtime stage
## -------------------
FROM eclipse-temurin:21-jre

# Install required system libraries
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y --no-install-recommends install libxml2 libfontconfig && \
    rm -rf /var/lib/apt/lists/*

# Add Tini for signal handling
ENV TINI_VERSION=v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "-s", "--"]

WORKDIR /opt/grobid

# Copy built artifacts from builder stage
COPY --from=builder /opt/grobid .

# Set Java options for GROBID service
ENV GROBID_SERVICE_OPTS="-Djava.library.path=grobid-home/lib/lin-64:grobid-home/lib/lin-64/jep --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.base/java.io=ALL-UNNAMED"

# Expose service port and admin port
EXPOSE 8070 8071

# Start the service
CMD ["./grobid-service/bin/grobid-service"]