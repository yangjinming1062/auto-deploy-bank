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

# Stage for creating JAR artifact
FROM alpine:latest AS jar-build

RUN apk add --no-cache zip openjdk17-jdk
RUN mkdir -p /artifacts
WORKDIR /build
COPY --from=go-build /kernel/kernel kernel
RUN mkdir -p META-INF && \
    echo -e "Manifest-Version: 1.0\nMain-Class: Main" > META-INF/MANIFEST.MF && \
    zip -r /artifacts/target.jar META-INF MANIFEST.MF kernel

FROM alpine:latest
LABEL maintainer="Liang Ding<845765@qq.com>"

RUN apk add --no-cache ca-certificates tzdata su-exec

ENV TZ=Asia/Shanghai
ENV HOME=/home/siyuan
ENV RUN_IN_CONTAINER=true
EXPOSE 6806

WORKDIR /opt/siyuan/
COPY --from=go-build --chmod=755 /kernel/kernel ./kernel
COPY --from=go-build --chmod=755 /kernel/entrypoint.sh ./entrypoint.sh
COPY --from=node-build /artifacts .
COPY --from=jar-build /artifacts/target.jar ./app.jar

RUN chmod +x /opt/siyuan/entrypoint.sh

ENTRYPOINT ["/opt/siyuan/entrypoint.sh"]
CMD ["/opt/siyuan/kernel"]