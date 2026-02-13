FROM node:20-alpine

WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install all dependencies (including dev for build)
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Expose the development server port
EXPOSE 8000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8000

# Start the development server (ws serves on port 8000 by default)
CMD ["npm", "start"]