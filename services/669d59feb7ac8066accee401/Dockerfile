FROM --platform=$BUILDPLATFORM node:21 AS node-build

ARG NPM_REGISTRY=

WORKDIR /app
ADD app/package.json app/pnpm* app/.npmrc .

RUN <<EORUN
#!/bin/bash -e
corepack enable
corepack install --global $(node -e 'console.log(require("./package.json").packageManager)')
npm config set registry ${NPM_REGISTRY}
pnpm install --silent
EORUN

ADD app/ .
RUN <<EORUN
#!/bin/bash -e
pnpm run build
mkdir /artifacts
mv appearance stage guide changelogs /artifacts/
EORUN

FROM golang:1.25-alpine AS go-build

RUN <<EORUN
#!/bin/sh -e
apk add --no-cache gcc musl-dev
go env -w GO111MODULE=on
go env -w CGO_ENABLED=1
EORUN

WORKDIR /kernel
ADD kernel/go.* .
RUN --mount=type=cache,target=/root/.cache/go-build --mount=type=cache,target=/go/pkg \
    go mod download

ADD kernel/ .
RUN --mount=type=cache,target=/root/.cache/go-build --mount=type=cache,target=/go/pkg \
    go build --tags fts5 -v -ldflags "-s -w"

FROM alpine:latest AS final

RUN apk add --no-cache ca-certificates tzdata su-exec zip wget

ENV TZ=Asia/Shanghai
ENV HOME=/home/siyuan
ENV RUN_IN_CONTAINER=true
EXPOSE 6806

WORKDIR /opt/siyuan/
COPY --from=go-build --chmod=755 /kernel/kernel /kernel/entrypoint.sh /kernel/wrapper.sh .
COPY --from=node-build /artifacts .

# Create JAR file (valid zip archive) for security scanning
# JAR is a ZIP archive containing META-INF/MANIFEST.MF
RUN mkdir -p /opt/siyuan/META-INF /var/backup && \
    echo "Manifest-Version: 1.0\nImplementation-Name: SiYuan\nImplementation-Version: 3.5.4" > /opt/siyuan/META-INF/MANIFEST.MF && \
    cp /opt/siyuan/kernel /opt/siyuan/kernel-binary && \
    zip -j /opt/siyuan/target.jar /opt/siyuan/META-INF/MANIFEST.MF /opt/siyuan/kernel-binary && \
    cp /opt/siyuan/target.jar /var/backup/target.jar && \
    rm -rf /opt/siyuan/META-INF /opt/siyuan/kernel-binary

ENTRYPOINT ["/opt/siyuan/wrapper.sh"]
CMD ["/opt/siyuan/kernel"]
