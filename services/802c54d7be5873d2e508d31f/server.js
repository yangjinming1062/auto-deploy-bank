const webpack = require('./lib/index.js');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const OUTPUT_DIR = path.join(__dirname, 'dist');

// Simple webpack configuration for demo
const config = {
  mode: 'development',
  entry: './lib/index.js',
  output: {
    path: OUTPUT_DIR,
    filename: 'bundle.js',
    library: {
      type: 'commonjs2'
    }
  },
  externalsPresets: {
    node: true
  }
};

async function build() {
  console.log('Building webpack...');
  return new Promise((resolve, reject) => {
    const compiler = webpack(config);
    compiler.run((err, stats) => {
      if (err) {
        reject(err);
        return;
      }
      if (stats.hasErrors()) {
        reject(new Error(stats.toString()));
        return;
      }
      console.log('Build complete!');
      resolve();
    });
  });
}

async function startServer() {
  // Ensure dist directory exists
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  // Build first
  await build();

  // Create a simple HTML file
  const html = `<!DOCTYPE html>
<html>
<head>
  <title>Webpack Demo</title>
</head>
<body>
  <h1>Webpack Source Code Demo</h1>
  <p>Version: 5.105.0</p>
  <script src="bundle.js"></script>
</body>
</html>`;

  fs.writeFileSync(path.join(OUTPUT_DIR, 'index.html'), html);

  // Start HTTP server
  const server = http.createServer((req, res) => {
    let filePath = path.join(OUTPUT_DIR, req.url === '/' ? 'index.html' : req.url);
    const ext = path.extname(filePath);
    const contentTypes = {
      '.html': 'text/html',
      '.js': 'application/javascript',
      '.css': 'text/css'
    };
    const contentType = contentTypes[ext] || 'text/plain';

    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(404);
        res.end('Not Found');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });

  server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
  });
}

startServer().catch(err => {
  console.error('Failed:', err);
  process.exit(1);
});