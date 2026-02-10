FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/761c56c09d24e19f004066e7

# Install bokeh and dependencies from PyPI
RUN pip install --no-cache-dir "bokeh>=3.0" Jinja2 contourpy numpy packaging pandas pillow pyyaml xyzservices

# Copy application files
COPY templates templates
COPY auth_module.py .

EXPOSE 5006

CMD ["bokeh", "serve", "--port", "5006", "--address", "0.0.0.0", "--auth-module", "auth_module.py"]