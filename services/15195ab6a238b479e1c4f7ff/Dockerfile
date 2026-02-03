# Multi-stage build for Gradle-based IntelliJ Plugin application
# Stage 1: Builder
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy Gradle wrapper
COPY CodeLocatorPlugin/gradle/wrapper /app/CodeLocatorPlugin/gradle/wrapper
COPY CodeLocatorPlugin/gradlew /app/CodeLocatorPlugin/gradlew

# Copy build configuration
COPY CodeLocatorPlugin/build.gradle.kts /app/CodeLocatorPlugin/build.gradle.kts
COPY CodeLocatorPlugin/settings.gradle.kts /app/CodeLocatorPlugin/settings.gradle.kts

# Copy the CodeLocatorModel from sibling directory
COPY CodeLocatorApp/CodeLocatorModel /app/CodeLocatorApp/CodeLocatorModel

# Copy source code
COPY CodeLocatorPlugin/src /app/CodeLocatorPlugin/src

# Copy local libs
COPY CodeLocatorPlugin/libs /app/CodeLocatorPlugin/libs

WORKDIR /app/CodeLocatorPlugin
RUN chmod +x gradlew

# Download dependencies
RUN ./gradlew dependencies --no-daemon -q

# Build classes
RUN ./gradlew clean classes :CodeLocatorModel:classes --no-daemon -q

# Create target.jar from compiled classes for security scanning
RUN cd /app && \
    jar cf target.jar -C CodeLocatorPlugin/build/classes/java/main . \
        -C CodeLocatorPlugin/build/resources/main . \
        -C CodeLocatorApp/CodeLocatorModel/build/classes/java/main .

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install bash for classpath building
RUN apk add --no-cache bash findutils

# Copy compiled classes
COPY --from=builder /app/CodeLocatorPlugin/build/classes/java/main /app/classes
COPY --from=builder /app/CodeLocatorPlugin/build/resources/main /app/resources
COPY --from=builder /app/CodeLocatorApp/CodeLocatorModel/build/classes/java/main /app/codelocator-model-classes

# Copy dependencies from gradle cache
COPY --from=builder /root/.gradle/caches /app/gradle-caches

# Copy local libs
COPY --from=builder /app/CodeLocatorPlugin/libs /app/libs

# Copy the target.jar for security scanning (volume mount)
COPY --from=builder /app/target.jar /app/target.jar

# Create a classpath script that finds all JARs
RUN echo '#!/bin/bash' > /app/classpath.sh && \
    echo 'CP="/app/classes:/app/codelocator-model-classes:/app/resources"' >> /app/classpath.sh && \
    echo 'for jar in $(find /app/gradle-caches -name "*.jar" 2>/dev/null); do' >> /app/classpath.sh && \
    echo '    CP="$CP:$jar"' >> /app/classpath.sh && \
    echo 'done' >> /app/classpath.sh && \
    echo 'for jar in /app/libs/*.jar; do' >> /app/classpath.sh && \
    echo '    [ -f "$jar" ] && CP="$CP:$jar"' >> /app/classpath.sh && \
    echo 'done' >> /app/classpath.sh && \
    echo 'echo $CP' >> /app/classpath.sh && \
    chmod +x /app/classpath.sh

# Expose the application port
EXPOSE 8080

# Run the application using all dependencies from gradle cache
CMD ["/bin/bash", "-c", "java -cp \"$(/app/classpath.sh)\" com.bytedance.tools.codelocator.CodeLocatorServer"]