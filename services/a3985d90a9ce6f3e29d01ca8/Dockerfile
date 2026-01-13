# Minima - On-Premises RAG System
# This is a multi-service project. Use docker-compose to launch individual services.
#
# Available deployment modes:
#   - docker-compose -f docker-compose-ollama.yml up --build  (Fully local with Ollama)
#   - docker-compose -f docker-compose-chatgpt.yml up --build  (ChatGPT integration)
#   - docker-compose -f docker-compose-mcp.yml up --build     (MCP Server integration)
#
# Build from individual service directories:
#   - indexer/    : Document indexing service (port 8001)
#   - llm/        : LLM service with RAG (port 40116)
#   - chat/       : React chat UI (port 3000)
#   - linker/     : ChatGPT integration (port 8003)
#   - mcp-server/ : MCP server for Claude Desktop

FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/a3985d90a9ce6f3e29d01ca8

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy deployment helper
COPY run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

EXPOSE 8001 40116 3000 8003

# Show usage info
CMD ["sh", "-c", "echo 'Minima RAG System' && echo 'Use docker-compose to launch services' && echo 'Available: docker-compose-ollama.yml, docker-compose-chatgpt.yml, docker-compose-mcp.yml' && sleep infinity"]