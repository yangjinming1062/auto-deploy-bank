# Copy WAR file for security scanning
FROM alpine:latest AS extractor

# Copy the built WAR from the contact-center image
COPY --from=cskefu/contact-center:develop /app/app.war /tmp/target.war

# Extract WAR contents and rename to target.jar
WORKDIR /tmp
RUN cp target.war target.jar

FROM scratch
COPY --from=extractor /tmp/target.jar /target.jar