#!/bin/bash
#
# Copyright © 2019 同程艺龙 (zhihui.li@ly.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

set -e

echo "Building Flower Center application..."
cd /home/ubuntu/deploy-projects/23925512b06c16b5890f4803

# Build the JAR file
mvn clean package -DskipTests -B -pl flower.center/flower.center.impl -am

# Copy the built JAR to target.jar for security scanning
cp flower.center/flower.center.impl/target/flower.center.impl-2.0.1.jar target.jar

echo "Build complete. Starting Docker containers..."
docker compose up -d