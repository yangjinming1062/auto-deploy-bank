FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl ffmpeg && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/ubuntu/deploy-projects/b59954b6825f729007ec90ec

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Upgrade huggingface_hub to be compatible with gradio
RUN pip install --no-cache-dir --upgrade huggingface_hub==0.25.0 gradio-client==1.3.0

# Patch gradio-client bug: TypeError when schema is boolean
# The get_type function needs to check if schema is a dict before calling .get() or using 'in' operator
RUN python3 << 'EOF'
utils_path = '/usr/local/lib/python3.10/site-packages/gradio_client/utils.py'

with open(utils_path, 'r') as f:
    content = f.read()

# Replace the entire get_type function with a fixed version
old_get_type = '''def get_type(schema: dict):
    if "const" in schema:
        return "const"
    if "enum" in schema:
        return "enum"
    elif "type" in schema:
        return schema["type"]
    elif schema.get("$ref"):
        return "$ref"
    elif schema.get("oneOf"):
        return "oneOf"
    elif schema.get("anyOf"):
        return "anyOf"
    elif schema.get("allOf"):
        return "allOf"
    elif "type" not in schema:
        return {}
    else:
        raise APIInfoParseError(f"Cannot parse type for {schema}")'''

new_get_type = '''def get_type(schema: dict):
    if not isinstance(schema, dict):
        return "any"
    if "const" in schema:
        return "const"
    if "enum" in schema:
        return "enum"
    elif "type" in schema:
        return schema["type"]
    elif schema.get("$ref"):
        return "$ref"
    elif schema.get("oneOf"):
        return "oneOf"
    elif schema.get("anyOf"):
        return "anyOf"
    elif schema.get("allOf"):
        return "allOf"
    elif "type" not in schema:
        return {}
    else:
        raise APIInfoParseError(f"Cannot parse type for {schema}")'''

content = content.replace(old_get_type, new_get_type)

# Also patch _json_schema_to_python_type to handle non-dict schemas
old_func_start = '''def _json_schema_to_python_type(schema: Any, defs) -> str:
    """Convert the json schema into a python type hint"""
    if schema == {}:
        return "Any"
    type_ = get_type(schema)'''

new_func_start = '''def _json_schema_to_python_type(schema: Any, defs) -> str:
    """Convert the json schema into a python type hint"""
    if schema == {} or not isinstance(schema, dict):
        return "Any"
    type_ = get_type(schema)'''

content = content.replace(old_func_start, new_func_start)

with open(utils_path, 'w') as f:
    f.write(content)

print("Patched get_type and _json_schema_to_python_type in gradio_client/utils.py")
EOF

# Copy application code
COPY app.py .
COPY setup.py .
COPY promptda/ ./promptda/
COPY torchhub/ ./torchhub/

# Install the package
RUN pip install -e .

# Expose Gradio default port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "app.py"]