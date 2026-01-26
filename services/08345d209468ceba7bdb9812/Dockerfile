# Builder stage - install all dependencies and build
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci --include=dev

COPY . .

# Patch createBusyAPI to make WebSocket connection optional (disabled by default)
RUN cat > src/common/services/createBusyAPI.js << 'EOF'
import { Client } from 'busyjs';

function createBusyAPI() {
  const url = process.env.BUSYJS_URL;
  if (!url) return null;
  const client = new Client(url);

  client.sendAsync = (message, params) =>
    new Promise((resolve, reject) => {
      client.call(message, params, (err, result) => {
        if (err !== null) return reject(err);
        return resolve(result);
      });
    });

  return client;
}

export default createBusyAPI;
EOF

# Patch store.js to handle null busyAPI
RUN sed -i 's/busyAPI: createBusyAPI(),/busyAPI: createBusyAPI() || {},/' src/client/store.js

ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build

# Production stage - only production runtime dependencies
FROM node:20-alpine

ENV NODE_ENV=production \
    PORT=3000 \
    STEEMCONNECT_CLIENT_ID=busy.app \
    STEEMCONNECT_REDIRECT_URL=http://localhost:3000/callback \
    STEEMCONNECT_HOST=https://steemconnect.com \
    STEEMJS_URL=https://api.steemit.com \
    SIGNUP_URL=https://signup.steemit.com/?ref=busy \
    MANIFEST_PATH=/assets \
    BUSYJS_URL=

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci --only=production && \
    rm -rf /usr/src/app/node_modules/.cache

COPY --from=builder /usr/src/app/build ./build
COPY --from=builder /usr/src/app/templates ./templates

EXPOSE 3000

CMD ["node", "build/server.js"]