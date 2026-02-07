FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/2c7c5273b6a01ebd5a2e44d8

# Install build dependencies for canvas and other native modules
RUN apk add --no-cache bash wget netcat-openbsd make g++ python3 pkgconf cairo-dev pango-dev jpeg-dev giflib-dev libpng-dev

# Copy package files for dependency caching
COPY package*.json ./

# Install dependencies (ignore canvas errors - optional for charting)
RUN npm ci --only=production --ignore-scripts || npm install --ignore-scripts --no-optional || true

# Copy source code
COPY . .

# Build the Pyret compiler (phaseA)
RUN make phaseA

# Create a simple HTTP server wrapper
COPY <<'EOF' server.js
const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 40126;
const PYRET_JARR = '/home/ubuntu/deploy-projects/2c7c5273b6a01ebd5a2e44d8/build/phaseA/pyret.jarr';
const CONFIG = '/home/ubuntu/deploy-projects/2c7c5273b6a01ebd5a2e44d8/src/scripts/standalone-configA.json';

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/run') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { code, args } = JSON.parse(body);
        const tempFile = path.join('/tmp', `pyret-${Date.now()}.arr`);
        fs.writeFileSync(tempFile, code);

        const proc = spawn('node', [
          '-max-old-space-size=8192',
          PYRET_JARR,
          '--run',
          tempFile,
          ...(args || [])
        ], {
          cwd: '/home/ubuntu/deploy-projects/2c7c5273b6a01ebd5a2e44d8',
          env: { ...process.env }
        });

        let stdout = '';
        let stderr = '';

        proc.stdout.on('data', d => stdout += d);
        proc.stderr.on('data', d => stderr += d);

        proc.on('close', (code) => {
          fs.unlinkSync(tempFile);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ stdout, stderr, exitCode: code }));
        });

        proc.on('error', (err) => {
          fs.unlinkSync(tempFile);
          res.writeHead(500);
          res.end(JSON.stringify({ error: err.message }));
        });
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else if (req.method === 'GET' && (req.url === '/' || req.url === '/health')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      service: 'Pyret Code Execution API',
      endpoints: {
        'POST /run': 'Execute Pyret code with {"code": "...", "args": []}'
      },
      version: '1.0.0'
    }));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found. POST /run with {"code": "...", "args": []}' }));
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Pyret server running on port ${PORT}`);
});
EOF

EXPOSE 40126

CMD ["node", "server.js"]