FROM node:20-alpine

WORKDIR /usr/local/app

# Install timezone data and build dependencies
RUN apk add --update --no-cache tzdata python3 make g++ && \
    chmod -R 777 /usr/local/app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy application source
COPY . .

# Build web UI
RUN npm run build

# Remove devDependencies to reduce image size
RUN npm prune --production --legacy-peer-deps

# Set environment variables
ENV NODE_ENV=production
ENV PORT=80
ENV TZ=Asia/Shanghai
ENV PATH=/usr/local/app/node_modules/.bin:/usr/local/app/script/Shell:$PATH

# Expose internal ports (only 80 exposed to host)
EXPOSE 80 8001 8002

# Start with pm2 in production mode
CMD ["pm2-runtime", "index.js", "-n", "elecV2P", "--no-daemon"]