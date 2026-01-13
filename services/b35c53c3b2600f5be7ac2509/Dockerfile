#
# The MIT License (MIT)
#
# Copyright (c) 2019 Code Technology Studio
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# Stage 1: Build frontend with full context
FROM node:20-alpine AS frontend-builder
WORKDIR /app
# Copy the entire project to have context for relative paths
COPY . .
# Go into the web-vue directory to build
WORKDIR /app/web-vue
RUN npm install
RUN npm run build

# Stage 2: Build backend
FROM maven:3.9-eclipse-temurin-17 AS backend-builder
WORKDIR /app
# Copy the entire project from the frontend-builder stage, which now includes the compiled frontend assets
COPY --from=frontend-builder /app .
# Now, the frontend assets are in the right place for maven to find them
RUN mvn clean package -DskipTests -B

# Stage 3: Create final image
FROM eclipse-temurin:17-jre-alpine
RUN apk add --no-cache icu-data-full
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
WORKDIR /app
# Copy the built JAR from the backend-builder stage
COPY --from=backend-builder /app/modules/server/target/server-2.11.1.jar ./target.jar
EXPOSE 2122
CMD ["sh", "-c", "cp /app/target.jar /export/target.jar && java -Dserver.servlet.encoding.charset=UTF-8 -Dserver.servlet.encoding.force=true -Dspring.web.resources.static-locations=classpath:/dist/,classpath:/META-INF/resources/,classpath:/resources/,classpath:/static/,classpath:/public/ -jar /app/target.jar"]
