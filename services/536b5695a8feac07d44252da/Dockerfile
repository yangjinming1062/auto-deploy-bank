FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install all dependencies (including devDependencies for webpack-dev-server)
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Start the development server
CMD ["yarn", "dev"]