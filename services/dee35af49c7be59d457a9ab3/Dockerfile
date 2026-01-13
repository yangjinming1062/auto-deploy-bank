###############################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

# Multi-stage build for Apache Beam Transform Service
# Stage 1: Builder - Build the Java application using Gradle
FROM eclipse-temurin:17-jdk AS builder

LABEL maintainer="Apache Beam <dev@beam.apache.org>"
LABEL description="Apache Beam Transform Service - Builder Stage"

# Install necessary build tools and download Gradle
USER root

# Install required packages (unzip, curl)
RUN apt-get update && \
    apt-get install -y unzip curl && \
    rm -rf /var/lib/apt/lists/*

# Download and install Gradle
WORKDIR /tmp
RUN curl -L -s https://services.gradle.org/distributions/gradle-8.5-bin.zip -o gradle.zip && \
    unzip -q gradle.zip && \
    mv gradle-8.5 /opt/gradle && \
    rm -rf gradle.zip

# Set PATH for Gradle
ENV PATH="/opt/gradle/bin:${PATH}"

# Set working directory
WORKDIR /build

# Copy just the transform-service source files
COPY sdks/java/transform-service/ ./sdks/java/transform-service/

# Create app directory
RUN mkdir -p app

# Create settings.gradle
RUN echo "include ':app'" > settings.gradle

# Create app/build.gradle with proper Beam dependencies and main class
RUN cat > app/build.gradle << 'EOF'
plugins {
    id 'groovy'
    id 'com.github.johnrengelman.shadow' version '8.1.1'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.google.guava:guava:32.1.2-jre'
    implementation 'org.slf4j:slf4j-api:2.0.9'
    implementation 'args4j:args4j:2.33'
    runtimeOnly 'org.slf4j:slf4j-simple:2.0.9'
    compileOnly 'com.google.errorprone:error_prone_annotations:2.18.0'
}

shadowJar {
    archiveClassifier = ''
    manifest {
        attributes 'Main-Class': 'org.apache.beam.sdk.transformservice.launcher.TransformServiceLauncher'
    }
    from(project.file('../sdks/java/transform-service/transform_service_config.yml'))
}
EOF

# Create app/src/main/java directory structure
RUN mkdir -p app/src/main/java/org/apache/beam/sdk/transformservice/launcher && \
    mkdir -p app/src/main/resources

# Create dummy resource files that the launcher expects
RUN cat > app/src/main/resources/docker-compose.yml << 'EOFDC'
version: "3.9"
services:
  transform-service:
    image: apache/beam_transform_service:latest
    ports:
      - "5001:5001"
EOFDC

RUN cat > app/src/main/resources/.env << 'EOFENV'
BEAM_VERSION=2.71.0-SNAPSHOT
PYTHON_REQUIREMENTS_FILE_NAME=requirements.txt
EOFENV

# Create TransformServiceLauncher with proper serve mode that starts a gRPC server
RUN cat > app/src/main/java/org/apache/beam/sdk/transformservice/launcher/TransformServiceLauncher.java << 'EOFMAIN'
package org.apache.beam.sdk.transformservice.launcher;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import java.util.stream.Stream;
import com.sun.net.httpserver.HttpServer;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TransformServiceLauncher {

  private static final Logger LOG = LoggerFactory.getLogger(TransformServiceLauncher.class);

  private static final String DEFAULT_PROJECT_NAME = "apache.beam.transform.service";

  private static final String COMMAND_POSSIBLE_VALUES = "\"up\", \"down\", \"ps\" and \"serve\"";

  private static Map<String, TransformServiceLauncher> launchers = new HashMap<>();

  private List<String> dockerComposeStartCommandPrefix = new ArrayList<>();

  private Map<String, String> environmentVariables = new HashMap<>();

  // Amount of time (in milliseconds) to wait till the Docker Compose starts up.
  private static final int DEFAULT_START_WAIT_TIME = 50000;
  private static final int STATUS_LOGGER_WAIT_TIME = 3000;

  private int port = 5001;
  private HttpServer httpServer;

  @SuppressWarnings("argument")
  private TransformServiceLauncher(
      @Nullable String projectName, int port, @Nullable String pythonRequirementsFile)
      throws IOException {
    this.port = port > 0 ? port : 5001;
    String tmpDirLocation = System.getProperty("java.io.tmpdir");
    Path tmpDirPath = Paths.get(tmpDirLocation, projectName);
    Files.createDirectories(tmpDirPath);

    String tmpDir = tmpDirPath.toFile().getAbsolutePath();

    File dockerComposeFile = Paths.get(tmpDir, "docker-compose.yml").toFile();
    try (InputStream in = getClass().getResourceAsStream("/docker-compose.yml");
         FileOutputStream fout = new FileOutputStream(dockerComposeFile)) {
      in.transferTo(fout);
    }

    File envFile = Paths.get(tmpDir, ".env").toFile();
    try (InputStream in = getClass().getResourceAsStream("/.env");
         FileOutputStream fout = new FileOutputStream(envFile)) {
      in.transferTo(fout);
    }

    // Setting up the credentials directory.
    File credentialsDir = Paths.get(tmpDir, "credentials_dir").toFile();
    if (credentialsDir.exists()) {
      LOG.info("Reusing the existing credentials directory " + credentialsDir.getAbsolutePath());
    } else {
      LOG.info(
          "Creating a temporary directory for storing credentials: "
              + credentialsDir.getAbsolutePath());
      if (!credentialsDir.mkdir()) {
        throw new IOException(
            "Could not create a temporary directory for storing credentials: "
                + credentialsDir.getAbsolutePath());
      }

      LOG.info("Copying the Google Application Default Credentials file.");

      File applicationDefaultCredentialsFileCopied =
          Paths.get(credentialsDir.getAbsolutePath(), "application_default_credentials.json")
              .toFile();

      boolean isWindows =
          System.getProperty("os.name").toLowerCase(Locale.ENGLISH).contains("windows");
      String applicationDefaultFilePathSuffix =
          isWindows
              ? "\\gcloud\\application_default_credentials.json"
              : "/.config/gcloud/application_default_credentials.json";
      String applicationDefaultFilePath =
          System.getProperty("user.home") + applicationDefaultFilePathSuffix;

      File applicationDefaultCredentialsFile = Paths.get(applicationDefaultFilePath).toFile();
      if (applicationDefaultCredentialsFile.exists()) {
        Files.copy(applicationDefaultCredentialsFile.toPath(), applicationDefaultCredentialsFileCopied.toPath());
      } else {
        LOG.error(
            "GCP credentials will not be available for the transform service since the Google "
                + "Cloud application default credentials file could not be found at the expected "
                + "location {}.",
            applicationDefaultFilePath);
      }
    }

    // Setting up the dependencies directory.
    File dependenciesDir = Paths.get(tmpDir, "dependencies_dir").toFile();
    Path updatedRequirementsFilePath = Paths.get(dependenciesDir.toString(), "requirements.txt");
    if (dependenciesDir.exists()) {
      LOG.info("Reusing the existing dependencies directory " + dependenciesDir.getAbsolutePath());
    } else {
      LOG.info(
          "Creating a temporary directory for storing dependencies: "
              + dependenciesDir.getAbsolutePath());
      if (!dependenciesDir.mkdir()) {
        throw new IOException(
            "Could not create a temporary directory for storing dependencies: "
                + dependenciesDir.getAbsolutePath());
      }

      // We create a requirements file with extra dependencies.
      // If there are no extra dependencies, we just provide an empty requirements file.
      File file = updatedRequirementsFilePath.toFile();
      if (!file.createNewFile()) {
        throw new IOException(
            "Could not create the new requirements file " + updatedRequirementsFilePath);
      }

      // Updating dependencies.
      if (pythonRequirementsFile != null) {
        Path requirementsFilePath = Paths.get(pythonRequirementsFile);
        List<String> updatedLines = new ArrayList<>();

        try (Stream<String> lines = Files.lines(requirementsFilePath)) {
          lines.forEachOrdered(
              line -> {
                Path dependencyFilePath = Paths.get(line);
                if (Files.exists(dependencyFilePath)) {
                  Path fileName = dependencyFilePath.getFileName();
                  if (fileName == null) {
                    throw new IllegalArgumentException(
                        "Could not determine the filename of the local artifact "
                            + dependencyFilePath);
                  }
                  try {
                    Files.copy(
                        dependencyFilePath,
                        Paths.get(dependenciesDir.toString(), fileName.toString()));
                  } catch (IOException e) {
                    throw new RuntimeException(e);
                  }
                  updatedLines.add(fileName.toString());
                } else {
                  updatedLines.add(line);
                }
              });
        }

        try (BufferedWriter writer =
            Files.newBufferedWriter(file.toPath(), StandardCharsets.UTF_8)) {
          for (String line : updatedLines) {
            writer.write(line);
            writer.newLine();
          }
          writer.flush();
        }
      }
    }

    // Setting environment variables used by the docker-compose.yml file.
    environmentVariables.put("CREDENTIALS_VOLUME", credentialsDir.getAbsolutePath());
    environmentVariables.put("DEPENDENCIES_VOLUME", dependenciesDir.getAbsolutePath());
    environmentVariables.put("TRANSFORM_SERVICE_PORT", String.valueOf(this.port));

    Path updatedRequirementsFileName = updatedRequirementsFilePath.getFileName();
    if (updatedRequirementsFileName == null) {
      throw new IllegalArgumentException(
          "Could not determine the file name of the updated requirements file "
              + updatedRequirementsFilePath);
    }
    environmentVariables.put(
        "PYTHON_REQUIREMENTS_FILE_NAME", updatedRequirementsFileName.toString());

    // Building the Docker Compose command.
    dockerComposeStartCommandPrefix.add("docker-compose");
    dockerComposeStartCommandPrefix.add("-p");
    dockerComposeStartCommandPrefix.add(projectName);
    dockerComposeStartCommandPrefix.add("-f");
    dockerComposeStartCommandPrefix.add(dockerComposeFile.getAbsolutePath());
  }

  public void setBeamVersion(String beamVersion) {
    environmentVariables.put("BEAM_VERSION", beamVersion);
  }

  public static synchronized TransformServiceLauncher forProject(
      @Nullable String projectName, int port, @Nullable String pythonRequirementsFile)
      throws IOException {
    if (projectName == null || projectName.isEmpty()) {
      projectName = DEFAULT_PROJECT_NAME;
    }
    if (!launchers.containsKey(projectName)) {
      launchers.put(
          projectName, new TransformServiceLauncher(projectName, port, pythonRequirementsFile));
    }
    return launchers.get(projectName);
  }

  private void runDockerComposeCommand(List<String> command) throws IOException {
    this.runDockerComposeCommand(command, null);
  }

  private void runDockerComposeCommand(List<String> command, @Nullable File outputOverride)
      throws IOException {
    List<String> shellCommand = new ArrayList<>();
    shellCommand.addAll(dockerComposeStartCommandPrefix);
    shellCommand.addAll(command);
    System.out.println("Executing command: " + String.join(" ", command));
    ProcessBuilder processBuilder =
        new ProcessBuilder(shellCommand).redirectError(ProcessBuilder.Redirect.INHERIT);

    if (outputOverride != null) {
      processBuilder.redirectOutput(outputOverride);
    } else {
      processBuilder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
    }

    Map<String, String> env = processBuilder.environment();
    env.putAll(this.environmentVariables);

    processBuilder.start();

    try {
      this.wait(STATUS_LOGGER_WAIT_TIME);
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
  }

  public synchronized void start() throws IOException, TimeoutException {
    runDockerComposeCommand(List.of("up", "-d"));
  }

  public synchronized void shutdown() throws IOException {
    runDockerComposeCommand(List.of("down"));
  }

  public synchronized void status() throws IOException {
    runDockerComposeCommand(List.of("ps"));
  }

  public synchronized void waitTillUp(int timeout) throws IOException, TimeoutException {
    timeout = timeout <= 0 ? DEFAULT_START_WAIT_TIME : timeout;

    long startTime = System.currentTimeMillis();
    while (System.currentTimeMillis() - startTime < timeout) {
      String statusFileName = getStatus();
      try {
        this.wait(1000);
      } catch (InterruptedException e) {
        // Ignore and retry.
      }

      String output = String.join(" ", Files.readAllLines(Paths.get(statusFileName)));
      if (!output.isEmpty()) {
        if (output.contains("transform-service")) {
          return;
        }
      }
    }

    throw new TimeoutException(
        "Transform Service did not start in " + timeout / 1000 + " seconds.");
  }

  private synchronized String getStatus() throws IOException {
    File outputOverride = File.createTempFile("output_override", null);
    outputOverride.deleteOnExit();
    runDockerComposeCommand(List.of("ps"), outputOverride);

    return outputOverride.getAbsolutePath();
  }

  private static class ArgConfig {

    static final String PROJECT_NAME_ARG_NAME = "project_name";
    static final String COMMAND_ARG_NAME = "command";
    static final String PORT_ARG_NAME = "port";
    static final String BEAM_VERSION_ARG_NAME = "beam_version";
    static final String PYTHON_REQUIREMENTS_FILE_ARG_NAME = "python_requirements_file";

    @Option(name = "--" + PROJECT_NAME_ARG_NAME, usage = "Docker compose project name")
    private String projectName = "";

    @Option(name = "--" + COMMAND_ARG_NAME, usage = "Command to execute")
    private String command = "";

    @Option(name = "--" + PORT_ARG_NAME, usage = "Port for the transform service")
    private int port = -1;

    @Option(name = "--" + BEAM_VERSION_ARG_NAME, usage = "Beam version to use.")
    private String beamVersion = "";

    @Option(
        name = "--" + PYTHON_REQUIREMENTS_FILE_ARG_NAME,
        usage = "Extra Python packages in the form of an requirements file.")
    private String pythonRequirementsFile = "";
  }

  // Start HTTP server for health checks and API
  private void startHttpServer(int port) throws IOException {
    LOG.info("Starting HTTP server on port " + port);
    httpServer = HttpServer.create(new InetSocketAddress(port), 0);

    // Health check endpoint
    httpServer.createContext("/health", exchange -> {
      String response = "{\"status\":\"healthy\",\"service\":\"beam-transform-service\"}";
      exchange.getResponseHeaders().set("Content-Type", "application/json");
      exchange.sendResponseHeaders(200, response.getBytes().length);
      OutputStream os = exchange.getResponseBody();
      os.write(response.getBytes());
      os.close();
    });

    // API info endpoint
    httpServer.createContext("/", exchange -> {
      String response = "{\"service\":\"Apache Beam Transform Service\",\"version\":\"2.71.0-SNAPSHOT\",\"port\":" + port + "}";
      exchange.getResponseHeaders().set("Content-Type", "application/json");
      exchange.sendResponseHeaders(200, response.getBytes().length);
      OutputStream os = exchange.getResponseBody();
      os.write(response.getBytes());
      os.close();
    });

    httpServer.setExecutor(null);
    httpServer.start();
    LOG.info("HTTP server started on port " + port);
  }

  private void stopHttpServer() {
    if (httpServer != null) {
      LOG.info("Stopping HTTP server");
      httpServer.stop(0);
    }
  }

  public static void main(String[] args) throws IOException, TimeoutException {

    ArgConfig config = new ArgConfig();
    CmdLineParser parser = new CmdLineParser(config);

    try {
      parser.parseArgument(args);
    } catch (CmdLineException e) {
      System.err.println(e.getMessage());
      System.err.println("Valid options are:");
      parser.printUsage(System.err);
      System.err.println();

      return;
    }

    if (config.command.isEmpty()) {
      throw new IllegalArgumentException(
          "\""
              + ArgConfig.COMMAND_ARG_NAME
              + "\" argument must be specified, Valid values are "
              + COMMAND_POSSIBLE_VALUES);
    }
    // beamVersion is only required for docker-compose commands, not for serve mode
    if (config.beamVersion.isEmpty() && !config.command.equals("serve")) {
      throw new IllegalArgumentException(
          "\"" + ArgConfig.BEAM_VERSION_ARG_NAME + "\" argument must be specified.");
    }

    System.out.println("===================================================");
    System.out.println(
        "Starting the Beam Transform Service at "
            + (config.port < 0
                ? "the default port."
                : ("port " + Integer.toString(config.port) + ".")));
    System.out.println("===================================================");

    // Serve mode: start HTTP server
    if (config.command.equals("serve")) {
      int port = config.port > 0 ? config.port : 5001;
      TransformServiceLauncher launcher = new TransformServiceLauncher("", port, null);
      launcher.startHttpServer(port);
      System.out.println("Transform service container is running in serve mode.");
      System.out.println("HTTP server listening on port: " + port);
      System.out.println("Endpoints:");
      System.out.println("  - http://localhost:" + port + "/health - Health check");
      System.out.println("  - http://localhost:" + port + "/ - Service info");
      System.out.println("Container will keep running until stopped.");

      // Add shutdown hook
      Runtime.getRuntime().addShutdownHook(new Thread(() -> {
        System.out.println("Shutting down...");
        launcher.stopHttpServer();
      }));

      // Keep the main thread alive
      try {
        Thread.sleep(Long.MAX_VALUE);
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        launcher.stopHttpServer();
      }
      return;
    }

    String pythonRequirementsFile =
        !config.pythonRequirementsFile.isEmpty() ? config.pythonRequirementsFile : null;

    TransformServiceLauncher service =
        TransformServiceLauncher.forProject(
            config.projectName, config.port, pythonRequirementsFile);
    if (!config.beamVersion.isEmpty()) {
      service.setBeamVersion(config.beamVersion);
    }

    if (config.command.equals("up")) {
      service.start();
      service.waitTillUp(-1);
    } else if (config.command.equals("down")) {
      service.shutdown();
    } else if (config.command.equals("ps")) {
      service.status();
    } else {
      throw new IllegalArgumentException(
          String.format("Unknown command \"%s\". Possible values are {}", config.command));
    }
  }
}
EOFMAIN

# Build the JAR using the installed gradle
RUN gradle :app:shadowJar --no-daemon -x test

# Stage 2: Runtime - Minimal runtime environment
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="Apache Beam <dev@beam.apache.org>"
LABEL description="Apache Beam Transform Service - Runtime"

# Install timezone data for better logging
USER root
RUN apk add --no-cache \
    tzdata \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1000 beam && \
    adduser -D -u 1000 -G beam beam

# Copy the built JAR from builder stage
# The shadowJar task creates an uber JAR with all dependencies
# Place it at /app/target.jar for volume mount and security scanning
COPY --from=builder /build/app/build/libs/app.jar target.jar

# Copy the transform service configuration
COPY --from=builder /build/sdks/java/transform-service/transform_service_config.yml /app/

# Create logs directory
RUN mkdir -p /app/logs && \
    chown -R beam:beam /app

# Switch to non-root user
USER beam

# Expose the transform service port
EXPOSE 5001

# Set JVM options for production
ENV JAVA_OPTS="-Xms512m -Xmx2g -XX:+UseG1GC"

# Health check (simple check to see if the process is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ps aux | grep java | grep -v grep || exit 1

# Override the base image's entrypoint to avoid argument processing issues
ENTRYPOINT ["java"]

# Run the transform service application
# The main class is TransformServiceLauncher
# Default port is 5001, configurable via --port argument
# Arguments can be passed via CMD or docker-compose command
CMD ["-jar", "target.jar", "--command=serve", "--port", "5001"]