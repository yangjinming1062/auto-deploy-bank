FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/86af56a1a25726b1d18b3302

# Install git (required by some dev dependencies)
RUN apk add --no-cache git

# Skip husky prepare script
ENV HUSKY=0

# Create .husky directory for husky prepare script
RUN mkdir -p .husky && \
    echo '# husky' > .husky/.gitkeep

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the project (generates dist/ folder)
RUN npm run build

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the sandbox server port
EXPOSE 3000

# Run the sandbox server
CMD ["node", "./sandbox/server.js"]