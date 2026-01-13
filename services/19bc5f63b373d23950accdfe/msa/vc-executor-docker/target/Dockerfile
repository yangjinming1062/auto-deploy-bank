#
# Copyright © 2016-2025 The Thingsboard Authors
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

FROM thingsboard/openjdk17:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -yq --no-install-recommends ncdu \
    && rm -rf /var/lib/apt/lists/*

COPY start-tb-vc-executor.sh tb-vc-executor.deb /tmp/

RUN mkdir -p /home/thingsboard/.config/jgit \
    && chown -R thingsboard:thingsboard /home/thingsboard \
    && chmod a+x /tmp/*.sh \
    && mv /tmp/start-tb-vc-executor.sh /usr/bin && \
    (yes | dpkg -i /tmp/tb-vc-executor.deb) && \
    rm /tmp/tb-vc-executor.deb && \
    (systemctl --no-reload disable --now tb-vc-executor.service > /dev/null 2>&1 || :) && \
    chmod 555 /usr/share/tb-vc-executor/bin/tb-vc-executor.jar

USER thingsboard

CMD ["start-tb-vc-executor.sh"]
