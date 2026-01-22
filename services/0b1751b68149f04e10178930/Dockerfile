# Stage 1: Build the we-vue library (without minification)
FROM node:20-alpine AS we-vue-builder

# Install Python and build tools
RUN apk add --no-cache python3 make g++ libc-dev

WORKDIR /app

# Copy root and we-vue package files
COPY package.json yarn.lock ./
COPY packages/we-vue/package*.json packages/we-vue/

# Install dependencies (skip native build scripts)
RUN yarn install --frozen-lockfile --ignore-scripts || yarn install --ignore-scripts

# Copy we-vue source
COPY packages/we-vue/ .

# Build we-vue library without minification to preserve 'h' parameter
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npx webpack --config build/config.js --progress --hide-modules --mode development

# Stage 2: Build the demo application
FROM node:20-alpine AS demo-builder

# Install Python and build tools
RUN apk add --no-cache python3 make g++ libc-dev

WORKDIR /app

# Copy demo package files and root files for dependencies
COPY package.json yarn.lock ./
COPY packages/demo/package*.json packages/demo/

# Install dependencies
RUN yarn install --frozen-lockfile --ignore-scripts || yarn install --ignore-scripts

# Copy built we-vue dist files
COPY --from=we-vue-builder /app/dist ./packages/we-vue/dist

# Create we-vue package for demo with a minimal postcss config
WORKDIR /app/packages/demo
RUN mkdir -p node_modules/we-vue/dist && \
    cp -r /app/packages/we-vue/dist/* node_modules/we-vue/dist/ && \
    echo 'module.exports = {}' > node_modules/we-vue/dist/postcss.config.js && \
    echo '{"name":"we-vue","version":"3.0.0-alpha.22","main":"dist/we-vue.js"}' > node_modules/we-vue/package.json

# Copy demo source
COPY packages/demo/ .

# Create vue.config.js with proper config to avoid thread-loader issues
# and disable minification
RUN cat > vue.config.js << 'EOF'
module.exports = {
  chainWebpack: config => {
    config.performance.set("hints", false)
    // Remove thread-loader for babel to avoid compatibility issues
    if (config.module.rule('js').use('thread-loader')) {
      config.module.rule('js').use('thread-loader').delete()
    }
  },
  lintOnSave: false,
  configureWebpack: {
    optimization: {
      minimize: false,  // Disable minification
    },
  },
}
EOF

# Build demo with environment variables
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npx vue-cli-service build --colors

# Note: render functions are now fixed in source files
# This sed fix handles any remaining edge cases
RUN cd /app/packages/demo/dist/js && \
    for f in *.js; do \
      sed -i 's/render: function ()/render: function (h)/g' "$f" && \
      sed -i 's/render = function ()/render = function (h)/g' "$f"; \
    done 2>/dev/null || true

# Stage 3: Serve with nginx
FROM nginx:alpine

# Copy nginx configuration
COPY packages/demo/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from demo builder stage
COPY --from=demo-builder /app/packages/demo/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]