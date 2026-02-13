FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies including webpack-cli which is required by bin/webpack.js
RUN yarn install --production=false

# Copy application files
COPY . .

# Set environment variables
ENV NODE_ENV=production

# Run webpack CLI (bin/webpack.js requires webpack-cli to be installed)
CMD ["node", "bin/webpack.js"]