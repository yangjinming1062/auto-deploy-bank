# Stage 1: Build with Gradle
FROM gradle:8-jdk17-alpine AS builder

# Set working directory
WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle gradle.properties ./
COPY gradle/wrapper/gradle-wrapper.properties gradle/wrapper/

# Remove the bintray plugin dependency (JCenter is deprecated/shut down)
# Create a patched build.gradle with all bintray references removed
RUN printf '%s\n' \
'if (project.hasProperty('\''overrideBuildEnvironment'\'')) {' \
'  apply from: project.overrideBuildEnvironment' \
'}' \
'' \
'buildscript {' \
'  repositories {' \
'    mavenCentral()' \
'    mavenLocal()' \
'  }' \
'}' \
'' \
'ext {' \
'  libs = [:]' \
'}' \
'' \
'libs += [' \
'    apache: "org.apache.commons:commons-lang3:3.4",' \
'    apacheCommonsIo: "commons-io:commons-io:2.4",' \
'    bcpkix: "org.bouncycastle:bcpkix-jdk15on:1.51",' \
'    bcprov: "org.bouncycastle:bcprov-jdk15on:1.51",' \
'    commonsCli: "commons-cli:commons-cli:1.2",' \
'    easymock: "org.easymock:easymock:3.3",' \
'    googleGuava: "com.google.guava:guava:18.0",' \
'    httpclient: "org.apache.httpcomponents:httpclient:4.3.1",' \
'    jacksonCodec: "com.fasterxml.jackson.core:jackson-core:2.5.3",' \
'    log4j: "log4j:log4j:1.2.17",' \
'    netty: "io.netty:netty-all:4.0.27.Final",' \
'    testng: "org.testng:testng:6.8.8",' \
'    restliServer: "com.linkedin.pegasus:restli-server:6.0.12",' \
'    restliNettyStandalone: "com.linkedin.pegasus:restli-netty-standalone:6.0.12"' \
']' \
'' \
'allprojects {' \
'    apply plugin: '\''java'\''' \
'    apply plugin: '\''maven-publish'\''' \
'' \
'    version='\''0.0.10'\''' \
'    group='\''com.linkedin.flashback'\''' \
'' \
'    dependencies {' \
'        implementation libs.apache' \
'        implementation libs.apacheCommonsIo' \
'        implementation libs.bcpkix' \
'        implementation libs.bcprov' \
'        implementation libs.commonsCli' \
'        implementation libs.easymock' \
'        implementation libs.googleGuava' \
'        implementation libs.httpclient' \
'        implementation libs.jacksonCodec' \
'        implementation libs.log4j' \
'        implementation libs.netty' \
'        testImplementation libs.testng' \
'    }' \
'    repositories {' \
'        mavenCentral()' \
'    }' \
'    test {' \
'        useTestNG()' \
'    }' \
'    tasks.withType(Jar) {' \
'        from "$rootDir/LICENSE"' \
'        from "$rootDir/NOTICE"' \
'    }' \
'    task sourcesJar(type: Jar) {' \
'        archiveClassifier = '\''sources'\''' \
'        from sourceSets.main.allSource' \
'    }' \
'    task javadocJar(type: Jar, dependsOn: javadoc) {' \
'        archiveClassifier = '\''javadoc'\''' \
'        from javadoc.destinationDir' \
'    }' \
'    publishing {' \
'        publications {' \
'            MyPublication(MavenPublication) {' \
'                from components.java' \
'                artifact javadocJar' \
'                artifact sourcesJar' \
'            }' \
'        }' \
'    }' \
'}' \
'' \
'project('\'':flashback-test-util'\'') {' \
'    dependencies {' \
'        implementation project('\'':flashback-core-impl'\'')' \
'        implementation project('\'':flashback-smartproxy'\'')' \
'        implementation project('\'':flashback-netty'\'')' \
'        implementation libs.testng' \
'    }' \
'}' \
'project('\'':flashback-smartproxy'\'') {' \
'    dependencies {' \
'        implementation project('\'':flashback-core-impl'\'')' \
'        implementation project('\'':flashback-netty'\'')' \
'        implementation project('\'':mitm'\'')' \
'    }' \
'}' \
'project('\'':flashback-netty'\'') {' \
'    dependencies {' \
'        implementation project('\'':flashback-core-impl'\'')' \
'    }' \
'}' \
'project('\'':flashback-admin'\'') {' \
'    dependencies {' \
'        implementation libs.restliServer' \
'        implementation libs.restliNettyStandalone' \
'        implementation project('\'':flashback-smartproxy'\'')' \
'    }' \
'    task startAdminServer(type: JavaExec) {' \
'        mainClass = '\''com.linkedin.restli.server.NettyStandaloneLauncher'\''' \
'        if (project.hasProperty('\''Args'\'')) {' \
'            args(Args.split())' \
'        }' \
'        args += ['\''-packages'\'', '\''com.linkedin.flashback'\'']' \
'        classpath = sourceSets.main.runtimeClasspath' \
'    }' \
'}' \
'project('\'':flashback-all'\'') {' \
'    dependencies {' \
'        implementation project('\'':flashback-core-impl'\'')' \
'        implementation project('\'':mitm'\'')' \
'        implementation project('\'':flashback-test-util'\'')' \
'        implementation project('\'':flashback-smartproxy'\'')' \
'        implementation project('\'':flashback-netty'\'')' \
'        implementation project('\'':flashback-admin'\'')' \
'    }' \
'}' > build.gradle

# Copy source code
COPY flashback-admin ./flashback-admin
COPY flashback-core-impl ./flashback-core-impl
COPY flashback-netty ./flashback-netty
COPY flashback-smartproxy ./flashback-smartproxy
COPY mitm ./mitm
COPY flashback-test-util ./flashback-test-util

# Create build.gradle for flashback-admin module with shadow plugin
RUN printf '%s\n' \
'plugins {' \
'    id '\''java'\''' \
'    id '\''com.github.johnrengelman.shadow'\'' version '\''8.1.1'\''' \
'}' \
'' \
'dependencies {' \
'    implementation project('\'':flashback-core-impl'\'')' \
'    implementation project('\'':flashback-netty'\'')' \
'    implementation project('\'':flashback-smartproxy'\'')' \
'    implementation project('\'':mitm'\'')' \
'    implementation '\''com.linkedin.pegasus:restli-server:6.0.12'\''' \
'    implementation '\''com.linkedin.pegasus:restli-netty-standalone:6.0.12'\''' \
'}' \
'' \
'shadowJar {' \
'    archiveBaseName.set('\''flashback-admin'\'')' \
'    mergeServiceFiles()' \
'    append '\''META-INF/LICENSE'\''' \
'    append '\''META-INF/NOTICE'\''' \
'    manifest {' \
'        attributes '\''Main-Class'\'': '\''com.linkedin.restli.server.NettyStandaloneLauncher'\''' \
'    }' \
'}' > flashback-admin/build.gradle

# Build the project and create a fat JAR using the shadow plugin
# Clean first to ensure all source files are recompiled
RUN gradle :flashback-admin:clean :flashback-admin:shadowJar --no-daemon -x test -Porg.gradle.jvmargs="-Xmx2g" && \
    cp /build/flashback-admin/build/libs/flashback-admin-*-all.jar /build/flashback-admin/build/libs/app.jar

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install iproute2 for ss command (needed for healthcheck)
RUN apk add --no-cache iproute2

# Create non-root user for security
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# Set working directory
WORKDIR /home/appuser

# Copy the fat JAR from builder stage
COPY --from=builder /build/flashback-admin/build/libs/app.jar app.jar

# Create directories for logs and data
RUN mkdir -p /home/appuser/logs && \
    chown -R appuser:appgroup /home/appuser

# Switch to non-root user
USER appuser

# Expose the admin server port (default 8080)
EXPOSE 8080

# Run the admin server with NettyStandaloneLauncher
# With tty: true and stdin_open: true, stdin will be kept open
# Bind to 0.0.0.0 to allow external IP access
CMD ["java", "-jar", "app.jar", "-host", "0.0.0.0", "-port", "8080", "-packages", "com.linkedin.flashback"]