FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install system dependencies for native modules
RUN apk add --no-cache python3 make g++

# Create package.json with Babel dependencies
RUN cat > package.json <<'EOF'
{
  "name": "babel-service",
  "version": "1.0.0",
  "type": "commonjs",
  "dependencies": {
    "@babel/core": "^8.0.0-beta.3",
    "@babel/preset-env": "^8.0.0-beta.3",
    "@babel/generator": "^8.0.0-beta.3",
    "@babel/traverse": "^8.0.0-beta.3",
    "@babel/types": "^8.0.0-beta.3",
    "@babel/parser": "^8.0.0-beta.3",
    "@babel/template": "^8.0.0-beta.3",
    "@babel/helpers": "^8.0.0-beta.3",
    "@babel/code-frame": "^8.0.0-beta.3",
    "gensync": "^1.0.0-beta.2",
    "semver": "^7.0.0",
    "commander": "^12.0.0"
  }
}
EOF

# Install dependencies using npm
RUN npm install

# Create a simple HTTP server using Babel packages
RUN cat > server.js <<'ENDSERVER'
const http = require("http");
const babel = require("@babel/core");

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Babel Transformation Service</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1 { color: #f5da55; }
    .container { display: flex; gap: 20px; }
    textarea { width: 50%; height: 400px; font-family: monospace; padding: 10px; }
    button { padding: 10px 20px; background: #f5da55; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
    button:hover { background: #e5ca45; }
    .result { margin-top: 20px; padding: 15px; background: #f5f5f5; border-radius: 4px; }
    .error { color: red; }
    .presets { margin-bottom: 10px; }
    label { display: inline-block; margin-right: 15px; }
  </style>
</head>
<body>
  <h1>🔧 Babel Transformation Service</h1>
  <p>Enter your JavaScript code and transform it using Babel presets.</p>

  <div class="container">
    <div>
      <h3>Input Code</h3>
      <textarea id="input" placeholder="Enter JavaScript code here...\n\nExample:\nconst message = \`Hello \${name}\`;\nconst { x, y } = point;\nclass Test {}\nconst double = (x) => x * 2;"></textarea>
    </div>
    <div>
      <h3>Transformed Code</h3>
      <textarea id="output" readonly placeholder="Transformed code will appear here..."></textarea>
    </div>
  </div>

  <div class="presets">
    <h3>Presets:</h3>
    <label><input type="checkbox" id="preset-env" checked> @babel/preset-env</label>
  </div>

  <div style="margin: 20px 0;">
    <button onclick="transform()">Transform Code</button>
  </div>

  <div id="result" class="result" style="display: none;"></div>

  <script>
    async function transform() {
      const input = document.getElementById("input").value;
      const output = document.getElementById("output");
      const result = document.getElementById("result");

      const presets = [];
      if (document.getElementById("preset-env").checked) {
        presets.push("@babel/preset-env");
      }

      output.value = "Transforming...";
      result.style.display = "none";

      try {
        const response = await fetch("/transform", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: input, presets })
        });

        const data = await response.json();

        if (response.ok) {
          output.value = data.code || "";
          result.className = "result";
          result.innerHTML = "<strong>✅ Transformation successful!</strong><br><br>" +
            "<strong>Output Code:</strong><br><pre style='background: white; padding: 10px; border-radius: 4px; overflow-x: auto;'>" +
            (data.code || "").replace(/</g, "&lt;").replace(/>/g, "&gt;") + "</pre>";
        } else {
          output.value = "";
          result.className = "result error";
          result.innerHTML = "<strong>❌ Error:</strong><br>" + (data.error || "Unknown error");
        }
        result.style.display = "block";
      } catch (err) {
        output.value = "";
        result.className = "result error";
        result.innerHTML = "<strong>❌ Network Error:</strong><br>" + err.message;
        result.style.display = "block";
      }
    }
  </script>
</body>
</html>`;

const server = http.createServer((req, res) => {
  if (req.method === "GET" && (req.url === "/" || req.url === "/index.html")) {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(html);
  } else if (req.method === "POST" && req.url === "/transform") {
    let body = "";
    req.on("data", chunk => body += chunk);
    req.on("end", () => {
      try {
        const { code, presets = ["@babel/preset-env"] } = JSON.parse(body);
        const result = babel.transformSync(code, {
          presets: presets
        });
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ code: result.code }));
      } catch (err) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
  } else if (req.url === "/health") {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("OK");
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

const PORT = process.env.PORT || 40081;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`Babel transformation service running on port ${PORT}`);
});
ENDSERVER

# Expose port
EXPOSE 40081

# Set environment
ENV NODE_ENV=production
ENV PORT=40081

# Run the server
CMD ["node", "server.js"]