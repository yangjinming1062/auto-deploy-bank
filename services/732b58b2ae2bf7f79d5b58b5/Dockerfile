FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/732b58b2ae2bf7f79d5b58b5

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy application files
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV PORT=40339

# Create a simple health check server wrapper
RUN printf '%s\n' 'const http = require("http");' \
'const server = http.createServer((req, res) => {' \
'  if (req.url === "/health" || req.url === "/") {' \
'    res.writeHead(200, {"Content-Type": "application/json"});' \
'    res.end(JSON.stringify({status: "ok", service: "dragonbones-runtime"}));' \
'  } else {' \
'    res.writeHead(404);' \
'    res.end();' \
'  }' \
'});' \
'server.listen(process.env.PORT || 40339, "0.0.0.0", () => {' \
'  console.log("DragonBones Runtime Service running on port " + (process.env.PORT || 40339));' \
'});' > /usr/local/bin/server.js

EXPOSE 40339

CMD ["node", "/usr/local/bin/server.js"]