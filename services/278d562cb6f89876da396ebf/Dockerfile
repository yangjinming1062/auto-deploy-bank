FROM node:20-alpine

# Install make for build process
RUN apk add --no-cache make

WORKDIR /home/ubuntu/deploy-projects/278d562cb6f89876da396ebf

# Copy package files
COPY package*.json ./

# Install dependencies (including dev for build)
RUN npm install

# Copy source and build
COPY . .
RUN chmod +x bin/lsc scripts/build-parser scripts/preroll scripts/test
RUN make force

# Set environment variables
ENV NODE_ENV=production

# Default command - run web server
CMD ["node", "server.js"]