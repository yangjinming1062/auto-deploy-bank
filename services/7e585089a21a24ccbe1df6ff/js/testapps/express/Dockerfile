# Production stage
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV PORT=4000

# Install express
RUN npm install express

# Copy server file
COPY server.js ./

# Expose the internal port
EXPOSE 4000

# Start the Express server
CMD ["node", "server.js"]
