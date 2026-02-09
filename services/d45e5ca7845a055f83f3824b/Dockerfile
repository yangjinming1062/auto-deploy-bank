FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/d45e5ca7845a055f83f3824b

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (needed for build and dev server)
RUN npm ci

# Copy source code
COPY . .

# Build the project
RUN npm run build

# Set environment variables
ENV NODE_ENV=production

# Expose the default ws port
EXPOSE 8000

# Run the dev server
CMD ["npm", "start"]