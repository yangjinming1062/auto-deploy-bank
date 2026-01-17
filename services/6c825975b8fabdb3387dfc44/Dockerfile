# Multi-stage build for Gradle-based Spring Boot application
# Stage 1: Builder with JDK - builds the JAR
FROM eclipse-temurin:17-jdk-alpine AS builder

# Set working directory
WORKDIR /build

# Install Gradle (using wrapper approach for compatibility)
RUN apk add --no-cache wget unzip bash && \
    wget -q https://services.gradle.org/distributions/gradle-7.6-bin.zip && \
    unzip gradle-7.6-bin.zip && \
    rm gradle-7.6-bin.zip && \
    ln -s /build/gradle-7.6/bin/gradle /usr/local/bin/gradle

# Copy dependency configuration
COPY build.gradle settings.gradle ./

# Create minimal settings.gradle with only required modules
RUN cat > settings.gradle << 'EOF'
rootProject.name = 'comsat'

include 'comsat-servlet'
include 'comsat-actors-api'
include 'comsat-spring:comsat-spring-webmvc'
include 'comsat-spring:comsat-spring-boot'
include 'comsat-spring:comsat-spring-boot:comsat-spring-boot-sample-tomcat'
EOF

# Create a minimal build.gradle without problematic plugins
RUN cat > build.gradle << 'EOF'
allprojects {
    repositories {
        mavenCentral()
    }
}

subprojects {
    apply plugin: 'java'

    sourceCompatibility = '1.8'
    targetCompatibility = '1.8'

    [compileJava, compileTestJava]*.options*.encoding = 'UTF-8'

    group               = "co.paralleluniverse"
    version             = "0.7.1-SNAPSHOT"
    description         = "Fibers services for web"

    repositories {
        mavenCentral()
        maven { url 'https://oss.sonatype.org/content/repositories/snapshots' }
    }

    dependencies {
        implementation "com.google.guava:guava:19.0"
        implementation "co.paralleluniverse:quasar-core:0.7.6"
        implementation "javax.servlet:javax.servlet-api:3.0.1"
    }
}

project (':comsat-actors-api') {
    dependencies {
        implementation "co.paralleluniverse:quasar-actors:0.7.6"
    }
}

project (':comsat-servlet') {
    dependencies {
        testRuntimeOnly "ch.qos.logback:logback-classic:1.1.3"
    }
}

project (':comsat-spring:comsat-spring-webmvc') {
    dependencies {
        implementation "co.paralleluniverse:quasar-core:0.7.6"
        implementation "org.springframework:spring-webmvc:4.2.5.RELEASE"
        implementation "org.springframework:spring-core:4.2.5.RELEASE"
        implementation "org.springframework:spring-context:4.2.5.RELEASE"
        implementation "org.springframework:spring-beans:4.2.5.RELEASE"
        implementation "org.springframework:spring-aop:4.2.5.RELEASE"
        implementation "org.springframework:spring-expression:4.2.5.RELEASE"
        implementation "commons-logging:commons-logging:1.2"
        implementation "javax.servlet:javax.servlet-api:3.0.1"
    }
}

project (':comsat-spring:comsat-spring-boot') {
    dependencies {
        implementation "org.springframework.boot:spring-boot:1.3.3.RELEASE"
        implementation ("org.springframework.boot:spring-boot-starter-web:1.3.3.RELEASE") {
            exclude group: 'org.springframework.boot', module: 'spring-boot-starter-tomcat'
        }
        implementation "org.springframework.boot:spring-boot-starter:1.3.3.RELEASE"
        implementation "org.springframework.boot:spring-boot-autoconfigure:1.3.3.RELEASE"
        implementation "org.springframework.boot:spring-boot-configuration-processor:1.3.3.RELEASE"
        implementation project(":comsat-spring:comsat-spring-webmvc")
    }
}

project (':comsat-spring:comsat-spring-boot:comsat-spring-boot-sample-tomcat') {
    dependencies {
        implementation project(":comsat-spring:comsat-spring-boot")
        runtimeOnly "org.springframework.boot:spring-boot-starter-tomcat:1.3.3.RELEASE"
    }
}
EOF

# Copy source code and build files
COPY comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src ./comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src
COPY comsat-actors-api/src ./comsat-actors-api/src
COPY comsat-spring/comsat-spring-webmvc/src ./comsat-spring/comsat-spring-webmvc/src
COPY comsat-spring/comsat-spring-boot/src ./comsat-spring/comsat-spring-boot/src
COPY comsat-servlet/src ./comsat-servlet/src

# Create application.properties with debug logging and Tomcat tuning
RUN mkdir -p comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources && \
    echo "server.port=8080" > comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources/application.properties && \
    echo "logging.level.root=DEBUG" >> comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources/application.properties && \
    echo "logging.level.org.springframework.web=DEBUG" >> comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources/application.properties && \
    echo "server.tomcat.max-keep-alive-requests=1" >> comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources/application.properties && \
    echo "server.tomcat.accept-count=10" >> comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/src/main/resources/application.properties

# Override sample build.gradle with shadowJar for fat JAR - use Undertow instead of Tomcat
RUN cat > comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/build.gradle << 'SAMPLE_EOF'
plugins {
    id 'com.github.johnrengelman.shadow' version '7.1.2'
}

ext {
    springBootVer = '1.3.3.RELEASE'
    springVer = '4.2.5.RELEASE'
    commonsLoggingVer = '1.2'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation project(":comsat-spring:comsat-spring-boot")
    implementation "org.springframework.boot:spring-boot:$springBootVer"
    implementation "org.springframework.boot:spring-boot-starter:$springBootVer"
    implementation "org.springframework.boot:spring-boot-starter-web:$springBootVer"
    implementation "org.springframework.boot:spring-boot-starter-actuator:$springBootVer"
    // Use Undertow instead of Tomcat for better Java 17 compatibility
    implementation "org.springframework.boot:spring-boot-starter-undertow:$springBootVer"
    implementation "commons-logging:commons-logging:$commonsLoggingVer"
    // Java 17+ compatibility - JAXB was removed from JDK
    implementation "javax.xml.bind:jaxb-api:2.3.1"
    implementation "org.glassfish.jaxb:jaxb-runtime:2.3.1"
    testImplementation "org.springframework.boot:spring-boot-starter-test:$springBootVer"
}

shadowJar {
    archiveFileName = 'app.jar'
    manifest {
        attributes 'Main-Class': 'comsat.sample.tomcat.SampleTomcatApplication'
    }
    mergeServiceFiles()
    // Ensure Spring Boot ServiceLoader files are preserved
    append 'META-INF/spring.factories'
    append 'META-INF/spring.handlers'
}
SAMPLE_EOF

# Build using shadowJar which creates a fat executable jar
RUN gradle :comsat-spring:comsat-spring-boot:comsat-spring-boot-sample-tomcat:shadowJar --no-daemon -x test

# Stage 2: Minimal runtime image
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Install required packages
RUN apk add --no-cache bash wget

# Copy the built JAR from builder stage
COPY --from=builder /build/comsat-spring/comsat-spring-boot/comsat-spring-boot-sample-tomcat/build/libs/app.jar /app/app.jar

# Create entrypoint script that copies JAR for security scanning
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'cp /app/app.jar /app/target.jar' >> /entrypoint.sh && \
    echo 'exec java "$@" -jar /app/app.jar' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose the port the app runs on (Spring Boot default port)
EXPOSE 8080

# Run the application with Java 17 module system options for Spring Boot 1.3.x + CGLIB + Tomcat compatibility
# Note: Quasar fiber support disabled due to Java 17 incompatibility
ENTRYPOINT ["/entrypoint.sh"]
CMD ["--add-opens=java.base/java.lang=ALL-UNNAMED", "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", "--add-opens=java.base/java.util=ALL-UNNAMED", "--add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED"]