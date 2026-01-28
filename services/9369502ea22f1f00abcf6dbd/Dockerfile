FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/9369502ea22f1f00abcf6dbd

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies (production only)
RUN npm install --omit=dev

# Copy application source
COPY . .

# Expose the application port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Start the application
CMD ["node", "./bin/www"]