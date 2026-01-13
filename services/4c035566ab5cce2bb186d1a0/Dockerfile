FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -r applications/multisource_rag_app/requirements.txt
RUN pip install --no-cache-dir gradio

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app/applications/multisource_rag_app/src"

CMD ["python", "src/agentscope/web/gradio/studio.py", "examples/dialogue_agent.py"]