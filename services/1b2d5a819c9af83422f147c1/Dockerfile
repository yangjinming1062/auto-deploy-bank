FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./
COPY demo/package.json ./demo/

# Install dependencies (this will create workspace symlinks)
RUN yarn install

# Install @stoplight/scripts explicitly as it's referenced in tsconfig but may not be installed
RUN yarn add -W -D @stoplight/scripts@10.0.0

# Copy source code (excluding node_modules via .dockerignore)
COPY . .

# Install missing dependencies and type definitions
RUN yarn add -W @fortawesome/free-solid-svg-icons@^6.5.0 @types/file-saver@^2.0.5 @types/urijs@^1.19.19 file-saver

# Expose the internal port
EXPOSE 4025

# Set environment variables
ENV NODE_ENV=production
ENV PORT=4025
ENV SKIP_PREFLIGHT_CHECK=true
ENV DOCKER_BUILD=true

# Start the demo application
CMD ["yarn", "workspace", "@stoplight/elements-demo", "start"]