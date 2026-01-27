FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/ed1356758b347400093a7f94

# Copy package files
COPY package*.json ./

# Install dependencies (no lock file, so use npm install)
RUN npm install

# Copy source code
COPY . .

# Build and test the project
RUN npm run build && npm run test-api

EXPOSE 3000

CMD ["node", "server.js"]