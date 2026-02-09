FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/802c54d7be5873d2e508d31f

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Copy package files first for better caching
COPY package.json yarn.lock ./

# Install dependencies using yarn
RUN yarn install --frozen-lockfile --production=false

# Copy application source
COPY lib lib/
COPY bin bin/
COPY hot hot/
COPY schemas schemas/
COPY server.js ./
COPY types.d.ts ./

# Expose the internal port
EXPOSE 3000

# Run the server
CMD ["node", "server.js"]