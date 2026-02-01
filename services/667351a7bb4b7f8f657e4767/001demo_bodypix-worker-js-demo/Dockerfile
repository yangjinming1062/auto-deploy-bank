FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies (including dev for build)
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install serve to host static files
RUN npm install -g serve

# Expose the port
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "/app/dist", "-l", "3000"]