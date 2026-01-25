# Builder stage - Build the adapter package
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock lerna.json .yarnrc tsconfig.json ./
COPY packages ./packages

# Install dependencies
RUN yarn install --frozen-lockfile

# Build the adapter package
RUN cd packages/adapter && yarn build

# Install esbuild for bundling demo
RUN npm install -g esbuild

# Create demo HTML with bundled JavaScript
RUN cat > index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Syllepsis Editor Demo</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 900px;
      margin: 0 auto;
      padding: 20px;
    }
    .editor-container {
      border: 1px solid #ddd;
      border-radius: 8px;
      padding: 20px;
      margin-top: 20px;
    }
    #editor {
      min-height: 200px;
      padding: 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
      margin-top: 10px;
    }
    .ProseMirror {
      outline: none;
      min-height: 150px;
    }
    .ProseMirror p {
      margin: 0 0 8px 0;
    }
    .info {
      background: #f5f5f5;
      padding: 15px;
      border-radius: 8px;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <h1>Syllepsis Editor Demo</h1>
  <div class="info">
    <p><strong>Syllepsis</strong> is a ProseMirror-based rich text editor framework.</p>
    <p>This demo shows the basic editor functionality using the adapter package.</p>
  </div>
  <div class="editor-container">
    <h3>Basic Editor</h3>
    <p>Start typing to use the editor...</p>
    <div id="editor" contenteditable="true">
      <p>Welcome to Syllepsis Editor!</p>
      <p>This is a <strong>basic demo</strong> showing the editor is working.</p>
      <p>Try typing some text above this paragraph.</p>
    </div>
  </div>
  <script src="demo-bundle.js"></script>
  <script>
    // Initialize a simple ProseMirror editor
    document.addEventListener('DOMContentLoaded', function() {
      const editorDiv = document.getElementById('editor');

      // Check if SylEditor is available
      if (typeof SylApi !== 'undefined') {
        console.log('Syllepsis Adapter loaded successfully');
        console.log('SylApi:', Object.keys(SylApi));

        // The adapter provides the core editor API
        // For a full editor with plugins, use the full @syllepsis/editor package
        editorDiv.addEventListener('input', function() {
          console.log('Editor content changed');
        });
      } else {
        console.error('Syllepsis Adapter not loaded');
      }
    });
  </script>
</body>
</html>
HTMLEOF

# Bundle the adapter for browser use
RUN esbuild \
  ./packages/adapter/dist/umd/index.js \
  --bundle \
  --outfile=demo-bundle.js \
  --format=iife \
  --global-name=SylApi \
  --platform=browser \
  --target=es2015 \
  --minify=false

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy built files
COPY --from=builder /app/index.html ./
COPY --from=builder /app/demo-bundle.js ./

# Set environment variables
ENV NODE_ENV=production
ENV PORT=5173
ENV HOST=0.0.0.0

# Expose the port
EXPOSE 5173

# Install http-server and run it
RUN npm install -g http-server

CMD ["http-server", "-p", "5173", "-c-1", "--host", "0.0.0.0", "."]