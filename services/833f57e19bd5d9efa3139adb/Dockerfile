# Use official n8n image as base
FROM n8nio/n8n:1.123.0-alpine

# Set environment variables
ENV NODE_ENV=production
ENV PORT=5678
ENV DB_TYPE=sqlite
ENV GENERIC_TIMEZONE=America/New_York

# Expose port
EXPOSE 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD node -e "fetch('http://localhost:5678/healthz').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

# Use the default n8n entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["n8n"]