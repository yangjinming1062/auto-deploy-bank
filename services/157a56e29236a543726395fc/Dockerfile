FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies (skip native node-sass build)
RUN npm ci --ignore-scripts

# Install sass as a drop-in replacement for node-sass
RUN npm install sass --save-dev

# Copy source code
COPY . .

# Create a vue.config.js that respects PUBLIC_PATH environment variable
RUN cat > vue.config.js << 'EOF'
const publicPath = process.env.PUBLIC_PATH;
module.exports = {
  publicPath: (publicPath !== undefined && publicPath !== null) ? publicPath : (process.env.NODE_ENV === 'production' ? '/flowy-vue/' : '/flowy-vue/'),
  productionSourceMap: process.env.NODE_ENV !== 'production',
  outputDir: 'docs',
};
EOF

# Build the demo with legacy OpenSSL provider
ENV NODE_OPTIONS=--openssl-legacy-provider
ENV PUBLIC_PATH=/
RUN npm run build:demo

# Install lightweight HTTP server
RUN npm install -g serve

# Production environment variables
ENV NODE_ENV=production
ENV PORT=40317

# Expose the port
EXPOSE 40317

# Run the server
CMD ["serve", "-s", "dist/demo", "-l", "40317"]