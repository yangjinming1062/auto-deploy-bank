FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/d6dc5d64b8e5c57b32be5f9c

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application files
COPY . .

# Create a simple server script for serving static files
RUN echo "const express = require('express'); \
const path = require('path'); \
const app = express(); \
const PORT = process.env.PORT || 8080; \
app.use(express.static(path.join(__dirname))); \
app.get('/', (req, res) => { res.sendFile(path.join(__dirname, 'index.html')); }); \
app.listen(PORT, '0.0.0.0', () => { console.log(\`Server running on port \${PORT}\`); });" > server.js

EXPOSE 8080

CMD ["node", "server.js"]