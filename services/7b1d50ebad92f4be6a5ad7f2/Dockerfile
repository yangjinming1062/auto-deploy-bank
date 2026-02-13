FROM oven/bun:1-alpine

WORKDIR /app

# Copy scripts
COPY scripts/ ./scripts/

# Make scripts executable
RUN chmod +x scripts/*.ts

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose the port
EXPOSE 3000

# Default command - runs the entrypoint
CMD ["bun", "scripts/server.ts"]