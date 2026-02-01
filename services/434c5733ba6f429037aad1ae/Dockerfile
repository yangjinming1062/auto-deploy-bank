FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000
ENV PUBLIC_URL=/

# Copy package files
COPY package*.json ./

# Copy the OpenJSCAD.org directory which contains local dependencies
COPY OpenJSCAD.org/ ./OpenJSCAD.org/

# Copy source code
COPY . .

# Create type declaration for lodash if missing
RUN mkdir -p src/types && echo "declare module 'lodash';" > src/types/lodash.d.ts

# Install all dependencies including dev dependencies for TypeScript build
RUN npm install

# Build the application
RUN npm run build

# Install serve to run the production build
RUN npm install -g serve

# Expose the port
EXPOSE 3000

# Start the server
CMD ["serve", "-s", "build", "-l", "3000"]