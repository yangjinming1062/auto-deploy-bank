# Use Node.js 20 Alpine base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    git \
    wget

# Copy yarn configuration and all necessary files
COPY package.json yarn.lock .yarnrc ./
COPY .yarn/releases/ .yarn/releases/

# Install dependencies at root
RUN yarn install --frozen-lockfile

# Copy source code before bootstrap
COPY . .

# Bootstrap the monorepo (prepare all packages)
RUN yarn bootstrap

# Build the gatsby package
RUN cd packages/gatsby && yarn build

# Copy example site and set up working directory
RUN cp -r examples/data-fetching /app/site
WORKDIR /app/site

# Install site dependencies
RUN yarn install

# Set environment variables
ENV NODE_ENV=development
ENV GATSBY_ACTIVE_ENV=development
ENV PORT=8000
ENV GATSBY_CPU_COUNT=auto
ENV PUBLIC_DIR=public
ENV HOST=localhost
ENV GATSBY_LOGGER=ink
ENV GATSBY_QUERY_ON_DEMAND=false
ENV GATSBY_TELEMETRY_DISABLED=0

# Expose port 8000
EXPOSE 8000

# Start Gatsby development server in the example site
CMD ["node", "/app/packages/gatsby/cli.js", "develop", "--port", "8000", "--host", "0.0.0.0"]