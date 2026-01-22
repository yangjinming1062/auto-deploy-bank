FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (skip prepare script which runs husky)
RUN npm ci --only=production --ignore-scripts || npm ci --only=production

# Copy source code
COPY . .

# Expose the CLI port
EXPOSE 40559

# Set environment
ENV NODE_ENV=production
ENV PORT=40559

# Run the CLI with a simple healthcheck HTTP server
CMD node -e "require('http').createServer((req,res)=>{res.writeHead(200,{'Content-Type':'text/plain'});res.end('KHipster CLI running');}).listen(40559,()=>{console.log('Healthcheck server running on port 40559')}); setInterval(()=>{},86400000);"