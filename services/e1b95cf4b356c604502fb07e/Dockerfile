# Dockerfile for HiBench 8.0-SNAPSHOT Big Data Benchmark Suite

# Stage 1: Builder - Build HiBench with Maven and Java 8
FROM ubuntu:22.04 AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    ssh \
    openjdk-8-jdk \
    maven \
    scala \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for Java 8
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Copy pom.xml and source code
COPY pom.xml .
COPY . .

# Build HiBench
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime - Final image with all dependencies
FROM maven:3.9-eclipse-temurin-11

# Install additional system dependencies for runtime
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    wget \
    python3 \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for runtime
ENV JAVA_HOME=/opt/java/openjdk

# Download and install Hadoop 3.2.0
ENV HADOOP_VERSION=3.2.0
ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt/ && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Create Hadoop environment configuration
RUN echo "export JAVA_HOME=/opt/java/openjdk" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_NAMENODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_DATANODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export HDFS_SECONDARYNAMENODE_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export YARN_NODEMANAGER_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    echo "export YARN_RESOURCEMANAGER_USER=root" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

# Download and install Spark 3.0.0
ENV SPARK_VERSION=3.0.0
ENV SPARK_HADOOP_VERSION=3.2
ENV SPARK_HOME=/opt/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}
RUN wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz && \
    tar xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz -C /opt/ && \
    rm spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz

# Set up SSH for Hadoop
RUN ssh-keygen -A && \
    mkdir -p /run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo 'root:password' | chpasswd

# Copy built artifacts from builder
COPY --from=builder /app /app

# Set up Hadoop environment
ENV JAVA_HOME=/opt/java/openjdk
ENV HADOOP_CONF_DIR=/app/conf
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin

# Create HDFS data directories
RUN mkdir -p /tmp/hadoop-root/dfs/name && \
    mkdir -p /tmp/hadoop-root/dfs/data && \
    mkdir -p /tmp/hadoop-root/dfs/temp

# Set HIBENCH_HOME
ENV HIBENCH_HOME=/app

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set +e\n\
\necho "Starting HiBench 8.0-SNAPSHOT..."\n\
\n\
# Set JAVA_HOME for all processes\nexport JAVA_HOME=/opt/java/openjdk\nexport HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_NODEMANAGER_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\n\
\n\
# Export Hadoop user environment variables\nexport JAVA_HOME=/opt/java/openjdk\nexport HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_NODEMANAGER_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\n\n\
# Start SSH service\n\
service ssh start || /usr/sbin/sshd\n\
\n\
# Format Hadoop namenode (only if not formatted)\n\
if [ ! -f "$HADOOP_HOME/etc/hadoop/hdfs/name/current/VERSION" ]; then\n\
    echo "Formatting Hadoop namenode..."\n\
    $HADOOP_HOME/bin/hdfs namenode -format -force\n\
fi\n\
\n\
# Start Hadoop services\n\
echo "Starting Hadoop HDFS..."\n\
$HADOOP_HOME/sbin/start-dfs.sh\n\
sleep 5\n\
\n\
echo "Starting Hadoop YARN..."\n\
$HADOOP_HOME/sbin/start-yarn.sh\n\
sleep 5\n\
\necho "Creating HDFS directories for HiBench..."\n\
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /HiBench\n\
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /HiBench\n\
\n\
# Wait for Hadoop to be ready\necho "Waiting for Hadoop to be ready..."\nsleep 10\n\
\n\
# Create a simple web interface on port 40146\necho "Setting up web interface on port 40146..."\n\
echo "HiBench 8.0-SNAPSHOT is running" > /app/status.html\n\
echo "<h1>HiBench 8.0-SNAPSHOT</h1>" >> /app/status.html\n\
echo "<p>Hadoop: $(hadoop version | head -1)</p>" >> /app/status.html\n\
echo "<p>Spark: $(spark-shell --version 2>&1 | head -1)</p>" >> /app/status.html\n\
\n\
# Start a simple HTTP server in background\n\
cd /app && python3 -m http.server 40146 > /dev/null 2>&1 &\n\
\n\
# Run the benchmark\necho "Running HiBench benchmarks..."\n\
cd /app\n\
./bin/run_all.sh\n\
\n\
# Keep container running\n\
echo "Benchmarks completed. Container is running."\n\
tail -f /dev/null\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose port 40146 for web interface
EXPOSE 40146

# Set working directory
WORKDIR /app

# Use entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]