FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY GradioDemo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create sitecustomize.py to patch HfFolder and gradio_client before any imports
RUN mkdir -p /usr/local/lib/python3.11/site-packages && \
    echo '# sitecustomize.py - runs automatically at Python startup' > /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo 'import sys' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '# Patch HfFolder' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo 'class _MockHfFolder:' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    @staticmethod' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    def save_token(token, token_path=None): pass' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    @staticmethod' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    def get_token(): return None' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    @staticmethod' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    def delete_token(): pass' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo 'import huggingface_hub' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo 'huggingface_hub.HfFolder = _MockHfFolder' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '# Patch gradio_client to handle boolean schemas' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo 'def _patch_gradio_client():' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    try:' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '        import gradio_client.utils as utils' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '        _original_json_schema_to_python_type = utils._json_schema_to_python_type' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '        def patched_json_schema_to_python_type(schema, defs=None):' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '            try:' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '                if isinstance(schema, bool):' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '                    return "bool"' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '                return _original_json_schema_to_python_type(schema, defs)' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '            except Exception:' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '                return "str"' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '        utils._json_schema_to_python_type = patched_json_schema_to_python_type' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '    except Exception:' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '        pass' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py && \
    echo '_patch_gradio_client()' >> /usr/local/lib/python3.11/site-packages/sitecustomize.py

# Copy application code
COPY GradioDemo/ .

# Expose Gradio default port
EXPOSE 7860

# Run the Gradio application
CMD ["python", "app.py"]