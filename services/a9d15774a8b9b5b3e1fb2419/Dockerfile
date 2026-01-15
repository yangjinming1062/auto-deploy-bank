FROM node:20-alpine

WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install all dependencies (need dev deps like vite for dev server)
RUN npm ci

# Copy source files
COPY . .

# Expose the internal port
EXPOSE 8080

# Set environment variables
ENV NODE_ENV=production
ENV PORT=8080
ENV VITE_PROD_SERVER=false

# Run the dev server (as specified in context)
CMD ["npm", "run", "dev", "--host"]