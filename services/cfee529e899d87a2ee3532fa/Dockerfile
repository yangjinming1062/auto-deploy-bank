FROM node:20-alpine

WORKDIR /app

# Install Python and build tools for native dependencies (deasync requires node-gyp)
RUN apk add --no-cache python3 make g++ build-base

# Copy package files
COPY package*.json ./

# Install dependencies (parcel-bundler is needed for start command)
RUN npm ci

# Copy application files
COPY . .

# Expose default Parcel port
EXPOSE 1234

# Set environment variables
ENV NODE_ENV=production
ENV PORT=1234

# Start Parcel dev server
CMD ["npm", "start"]