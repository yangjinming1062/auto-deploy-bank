FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/3fcd55f8adb21befd0be6c9c

# Copy root package files first
COPY package.json package-lock.json ./

# Copy website package files
COPY website/package*.json website/

# Install dependencies (skip postinstall scripts)
RUN npm ci --workspaces --ignore-scripts

# Copy website source files to the website directory
COPY website/ ./website/

# Copy packages needed for doc generation
COPY packages/ ./packages/

# Build the Docusaurus site using docusaurus build
WORKDIR /home/ubuntu/deploy-projects/3fcd55f8adb21befd0be6c9c/website
RUN npm run gen-docs && npx docusaurus build

# Switch to website directory for serving
WORKDIR /home/ubuntu/deploy-projects/3fcd55f8adb21befd0be6c9c/website

# Expose the default Docusaurus serve port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Run Docusaurus serve (foreground process)
CMD ["npx", "docusaurus", "serve", "--port", "3000", "--host", "0.0.0.0"]