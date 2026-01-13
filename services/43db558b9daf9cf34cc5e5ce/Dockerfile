FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and gulpfile
COPY yarn.lock ./
COPY package.json ./
COPY gulpfile.js ./

# Install all dependencies (including devDependencies for Express)
RUN yarn install --dev

# Copy generator code
COPY . .

# Create a simple documentation server
RUN echo 'const express = require("express"); \
const app = express(); \
const PORT = process.env.PORT || 3000; \
app.get("/", (req, res) => { \
  res.send(`<!DOCTYPE html> \
<html> \
<head><title>Generator-REST</title></head> \
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;"> \
<h1>Generator-REST</h1> \
<p>A Yeoman generator that scaffolds RESTful API projects using Node.js, Express, and MongoDB/Mongoose.</p> \
<h2>Generators Available:</h2> \
<ul> \
  <li><strong>yo rest</strong> - Creates new REST API projects</li> \
  <li><strong>yo rest:api</strong> - Creates new API endpoints within generated projects</li> \
</ul> \
<h2>Quick Start:</h2> \
<ol> \
  <li>Install Yeoman: <code>npm install -g yo</code></li> \
  <li>Install generator: <code>npm install -g generator-rest</code></li> \
  <li>Run generator: <code>yo rest</code></li> \
</ol> \
<h2>Tests:</h2> \
<p>Run tests with: <code>npm test</code></p> \
<p>Run linting with: <code>npm run lint</code></p> \
<h2>Documentation:</h2> \
<p>For detailed documentation, visit the GitHub repository.</p> \
</body> \
</html>`); \
}); \
app.listen(PORT, () => console.log(`Generator-REST server running on port ${PORT}`));' > server.js

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose port
EXPOSE 3000

# Run the documentation server by default
CMD ["node", "server.js"]