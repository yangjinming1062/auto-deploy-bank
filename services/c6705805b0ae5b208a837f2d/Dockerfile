FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy application files
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Change ownership of the working directory
RUN chown -R nodejs:nodejs /home/ubuntu/deploy-projects

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Start the service
CMD ["node", "server.js"]