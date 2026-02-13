const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8080;

const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Webpack Dev Server</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    h1 { color: #8ed6f5; }
    .status { background: #d4edda; padding: 15px; border-radius: 5px; }
  </style>
</head>
<body>
  <h1>Webpack Development Server</h1>
  <div class="status">Service is running successfully!</div>
  <p>Version: 5.105.2</p>
</body>
</html>
`;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(html);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}/`);
});