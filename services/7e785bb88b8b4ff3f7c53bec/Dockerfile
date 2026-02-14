# Stage 1: Build stage
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files first
COPY package.json yarn.lock ./

# Copy scripts first (needed for yarn workspace symlinks)
COPY scripts ./scripts

# Install dependencies (including workspace packages via postinstall)
RUN yarn install --frozen-lockfile

# Copy the entire project
COPY . .

# Re-run yarn install to properly link all workspace packages
RUN yarn install --frozen-lockfile

# Fix package.json locations for packages with package.json in subdirectories
RUN cat > /fix-packages.js << 'ENDOFFILE'
const fs = require('fs');
const path = require('path');

function findPackageJsonFiles(dir, results) {
  results = results || [];
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === 'node_modules') continue;

        const pkgPath = path.join(fullPath, 'package.json');
        if (fs.existsSync(pkgPath)) {
          results.push(pkgPath);
          continue;
        }

        findPackageJsonFiles(fullPath, results);
      }
    }
  } catch (e) {
    // Ignore errors
  }
  return results;
}

const reactComponentsDir = 'packages/react-components';
const pkgFiles = [];
findPackageJsonFiles(reactComponentsDir, pkgFiles);

for (const pkgFile of pkgFiles) {
  const pkgContent = fs.readFileSync(pkgFile, 'utf-8');
  const pkg = JSON.parse(pkgContent);
  const pkgName = pkg.name;

  const pkgDir = pkgName.split('/')[1];
  const targetDir = path.join('node_modules/@fluentui', pkgDir);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }
  const targetFile = path.join(targetDir, 'package.json');
  if (!fs.existsSync(targetFile)) {
    fs.copyFileSync(pkgFile, targetFile);
  }
}
ENDOFFILE
RUN node /fix-packages.js

# Build the essential packages that react-components depends on
# These are the packages that Storybook in public-docsite-v9 needs
RUN yarn nx run react-alert:build 2>/dev/null || true && \
    yarn nx run react-infobutton:build 2>/dev/null || true && \
    yarn nx run react-virtualizer:build 2>/dev/null || true && \
    yarn nx run react-components:build 2>/dev/null || true && \
    yarn nx run storybook-llms-extractor:build 2>/dev/null || true

# Build the react-storybook-addon packages that Storybook depends on
RUN yarn nx run-many --target=build --projects=react-storybook-addon,react-storybook-addon-export-to-sandbox --parallel=2

# Build Storybook documentation site (skip postbuild which requires Playwright)
RUN cd apps/public-docsite-v9 && yarn cross-env NODE_OPTIONS=--max_old_space_size=3072 DEPLOY_PATH=/react/ npx storybook build -o ./dist/react --docs

# Stage 2: Production stage
FROM node:22-alpine AS production

WORKDIR /app

# Install serve for serving static files
RUN npm install -g serve

# Copy built Storybook from builder stage
COPY --from=builder /app/apps/public-docsite-v9/dist/react /app/dist

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose port
EXPOSE 3000

# Run serve to host the static files
CMD ["serve", "-s", "/app/dist", "-l", "tcp://0.0.0.0:3000", "--no-clipboard"]