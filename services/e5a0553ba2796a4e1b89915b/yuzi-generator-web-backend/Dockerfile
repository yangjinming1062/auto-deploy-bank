# Docker 镜像构建
# @author <a href="https://github.com/liyupi">程序员鱼皮</a>
# @from <a href="https://yupi.icu">编程导航知识星球</a>

# Runtime
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy the pre-built JAR
COPY target/*.jar target.jar

# Expose port
EXPOSE 8120

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8120/api/doc.html || exit 1

# Run the application
CMD ["java", "-jar", "target.jar", "--spring.profiles.active=prod"]