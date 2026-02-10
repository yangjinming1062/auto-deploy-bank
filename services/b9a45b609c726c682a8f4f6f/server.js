const http = require('http');
const jsonpath = require('./index.js');

const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && (req.url === '/' || req.url === '/health')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'jsonpath-api' }));
  } else if (req.method === 'POST' && req.url === '/query') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const { json, path } = JSON.parse(body);
        const result = jsonpath.query(json, path);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ result }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not found. POST to /query with {json, path}' }));
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`JSONPath API server running on port ${PORT}`);
});