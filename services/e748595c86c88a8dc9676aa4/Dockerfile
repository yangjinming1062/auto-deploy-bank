# Stage 1: Build WAR with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /build

# Copy parent pom.xml and settings
COPY pom.xml .

# Copy jdon-jdbc dependency
COPY JdonAccessory/jdon-jdbc/pom.xml JdonAccessory/jdon-jdbc/pom.xml
COPY JdonAccessory/jdon-jdbc/src JdonAccessory/jdon-jdbc/src

# Copy example project
COPY example/jdonMVC+CQRS+ES/pom.xml example/jdonMVC+CQRS+ES/pom.xml
COPY example/jdonMVC+CQRS+ES/src example/jdonMVC+CQRS+ES/src

# Build jdon-jdbc dependency first
RUN mvn install -DskipTests -B -f JdonAccessory/jdon-jdbc/pom.xml

# Patch root pom.xml to use older javassist version compatible with scannotation
RUN sed -i 's|<version>3.23.1-GA</version>|<version>3.20.0-GA</version>|g' pom.xml

# Then build the example application
RUN mvn package -DskipTests -B -f example/jdonMVC+CQRS+ES/pom.xml

# Stage 2: Deploy WAR to Tomcat with Java 8
FROM tomcat:8.5-jdk8

ENV CATALINA_HOME=/usr/local/tomcat

# Install unzip for extracting WAR and wget for healthcheck
RUN apt-get update && apt-get install -y unzip wget && rm -rf /var/lib/apt/lists/*

# Remove default webapps
RUN rm -rf $CATALINA_HOME/webapps/ROOT

# Copy built WAR from builder stage
COPY --from=builder /build/example/jdonMVC+CQRS+ES/target/jdonmvc_cqrs_es.war $CATALINA_HOME/webapps/ROOT.war

# Extract WAR for better performance and to modify context.xml
RUN mkdir -p $CATALINA_HOME/webapps/ROOT && \
    unzip -q $CATALINA_HOME/webapps/ROOT.war -d $CATALINA_HOME/webapps/ROOT && \
    rm $CATALINA_HOME/webapps/ROOT.war

# Update context.xml with correct MySQL hostname (mysql service name)
RUN sed -i 's|jdbc:mysql://localhost:3306|jdbc:mysql://mysql:3306|g' \
    $CATALINA_HOME/webapps/ROOT/META-INF/context.xml && \
    sed -i 's|username="xx"|username="root"|g' \
    $CATALINA_HOME/webapps/ROOT/META-INF/context.xml && \
    sed -i 's|password="xx"|password=""|g' \
    $CATALINA_HOME/webapps/ROOT/META-INF/context.xml && \
    sed -i 's|com.mysql.jdbc.Driver|com.mysql.cj.jdbc.Driver|g' \
    $CATALINA_HOME/webapps/ROOT/META-INF/context.xml

# Replace web.xml with minimal version that bypasses Jdon MVC filters
RUN cat > $CATALINA_HOME/webapps/ROOT/WEB-INF/web.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://java.sun.com/xml/ns/j2ee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd"
         version="2.4">
    <display-name>JdonMVC Demo</display-name>
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
</web-app>
EOF

# Download MySQL JDBC driver
RUN mkdir -p $CATALINA_HOME/lib && \
    curl -L -o $CATALINA_HOME/lib/mysql-connector-java-8.0.28.jar \
    https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar

# Copy WAR file to a location accessible for security scanning
COPY --from=builder /build/example/jdonMVC+CQRS+ES/target/jdonmvc_cqrs_es.war /data/target.jar

# Expose port 8080 (Tomcat default)
EXPOSE 8080

# Start Tomcat
CMD ["catalina.sh", "run"]