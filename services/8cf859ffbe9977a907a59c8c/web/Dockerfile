####################
# 公共基础阶段
####################
FROM node:22.17.0 AS base

WORKDIR /app
ENV PNPM_SKIP_PROMPT=true
ENV CI=true

RUN corepack enable && corepack prepare pnpm@10.10.0 --activate

COPY . .

#COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --frozen-lockfile

# 拷贝项目

#RUN pnpm i

# 安装 pnpm
#RUN corepack enable && corepack prepare pnpm@latest --activate
#
## 清理依赖缓存
#RUN pnpm store prune && rm -rf $(pnpm store path) && \
#    rm -rf node_modules .npmrc package-lock.json pnpm-lock.yaml .pnpm-store .turbo && \
#    find . -name 'node_modules' -type d -prune -exec rm -rf '{}' +
#
##RUN pnpm run clean
#
## 安装依赖
##RUN pnpm install --force



####################
# 开发阶段
####################
# 默认启动 dev server
FROM base AS dev

# 暴露端口（根据需要）
EXPOSE 5678
#CMD ["tail", "-f", "/dev/null"]

# 启动开发服务器
CMD ["npm", "run", "dev:antd"]

# --- 构建阶段 ---
FROM base AS build

# 构建生产版本
RUN npm run build:antd

# --- 生产阶段 ---
FROM nginx:1.25-alpine AS prod

# 删除默认配置
RUN rm -rf /usr/share/nginx/html/*

# 从构建阶段拷贝打包产物到 nginx html 目录
COPY --from=build /app/apps/web-antd/dist /usr/share/nginx/html

# 如果有需要，也可以拷贝自定义 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 5268

# 默认启动 nginx
CMD ["nginx", "-g", "daemon off;"]
