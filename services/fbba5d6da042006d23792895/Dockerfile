FROM node:20-alpine

WORKDIR /home

# Copy package files from snippets directory
COPY snippets/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files from snippets directory
COPY snippets/ ./

# Expose port
EXPOSE 8080

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8080

# Start http-server
CMD ["npx", "http-server", "--cors", ".", "-p", "8080"]