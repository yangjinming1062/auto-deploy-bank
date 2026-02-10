FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/985e5b069a091ea20a51e0a4

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create templates directory
RUN mkdir -p templates

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Start the server
CMD ["node", "server.js"]