FROM python:3.10-slim

# Install curl, Node.js, npm and build essentials
RUN apt-get update && apt-get install -y curl nodejs npm build-essential && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm@10.x

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME=0.0.0.0

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install Gradio in editable mode
RUN pip install -e .

# Build frontend
RUN pnpm i --frozen-lockfile --ignore-scripts && pnpm build

# Create a simple app.py that won't be overwritten
RUN cat > /app/app.py << 'EOF'
import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
EOF

# Expose the port Gradio runs on
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Run the app
CMD ["python", "app.py"]