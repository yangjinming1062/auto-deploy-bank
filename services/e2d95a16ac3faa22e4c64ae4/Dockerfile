# Production stage - using pre-built assets
FROM node:20-alpine

WORKDIR /app

# Install serve for static file serving
RUN npm install -g serve

# Copy built artifacts
COPY bin ./bin
COPY *.html ./

EXPOSE 80

CMD ["serve", "-l", "80", "-s", "."]