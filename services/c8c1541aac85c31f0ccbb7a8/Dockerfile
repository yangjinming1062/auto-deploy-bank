FROM node:20-alpine

# Install timezone data
RUN apk add --update --no-cache tzdata

WORKDIR /usr/local/app

# Copy package files and install production dependencies
COPY package*.json ./
RUN npm install --only=production --legacy-peer-deps

# Copy application source
COPY . .

# Set permissions
RUN chmod -R 777 /usr/local/app

# Environment variables
ENV NODE_ENV=production
ENV PORT=80
ENV TZ=Asia/Shanghai
ENV PATH=/usr/local/app/node_modules/.bin:$PATH

# Expose internal ports (only 80 exposed to host)
EXPOSE 80 8001 8002

# Use pm2-runtime for production process management
CMD ["pm2-runtime", "index.js", "-n", "elecV2P", "--no-daemon"]