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

COPY start-tb-http-transport.sh tb-http-transport.deb /tmp/

RUN chmod a+x /tmp/*.sh \
    && mv /tmp/start-tb-http-transport.sh /usr/bin && \
    (yes | dpkg -i /tmp/tb-http-transport.deb) && \
    rm /tmp/tb-http-transport.deb && \
    (systemctl --no-reload disable --now tb-http-transport.service > /dev/null 2>&1 || :) && \
    chmod 555 /usr/share/tb-http-transport/bin/tb-http-transport.jar

USER thingsboard

CMD ["start-tb-http-transport.sh"]
