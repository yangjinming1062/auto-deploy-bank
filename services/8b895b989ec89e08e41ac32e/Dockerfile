FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/8b895b989ec89e08e41ac32e

# Install dependencies
COPY package*.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy source and build
COPY . .
RUN yarn build

# Expose port for serving built files
EXPOSE 41087

# Start a simple HTTP server to serve built library files
WORKDIR /home/ubuntu/deploy-projects/8b895b989ec89e08e41ac32e/dist
CMD ["npx", "http-server", ".", "-p", "41087", "-c-1"]