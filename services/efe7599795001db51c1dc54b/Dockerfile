FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/efe7599795001db51c1dc54b

# Copy package files for dependency caching
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy application source code
COPY . .

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Expose internal port
EXPOSE 3000

# Start the application
CMD ["node", "app.js"]