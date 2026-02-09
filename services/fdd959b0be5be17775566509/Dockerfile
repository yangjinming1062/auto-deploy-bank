FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Copy project structure
COPY packages ./packages
COPY extensions ./extensions
COPY translations ./translations

# Install all dependencies (needed for build)
RUN npm install

# Compile the source code with SWC
RUN npm run compile && npm run compile:db

# Build the project
RUN npm run build

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Expose the application port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "start"]