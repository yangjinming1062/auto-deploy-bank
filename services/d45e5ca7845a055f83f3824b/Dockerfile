FROM node:20-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/d45e5ca7845a055f83f3824b

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8000

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (including dev for build)
RUN npm install

# Copy source code
COPY . .

# Build the project
RUN npm run build

# Expose the port the web server runs on
EXPOSE 8000

# Start the web server
CMD ["npm", "start"]