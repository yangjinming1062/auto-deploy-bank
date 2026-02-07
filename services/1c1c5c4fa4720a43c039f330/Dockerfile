# Use Tomcat as base image for WAR deployment with JSP support
FROM tomcat:10-jdk17

# Remove default Tomcat webapps
RUN rm -rf /usr/local/tomcat/webapps/*

# Set timezone
ENV TZ=Asia/Shanghai

# Configure Tomcat to use port 8081
RUN sed -i 's/Connector port="8080"/Connector port="8081"/' /usr/local/tomcat/conf/server.xml

# Copy WAR file to webapps ROOT
COPY target/newblog.war /usr/local/tomcat/webapps/ROOT.war

# Expose port
EXPOSE 8081

# Start Tomcat
CMD ["catalina.sh", "run"]