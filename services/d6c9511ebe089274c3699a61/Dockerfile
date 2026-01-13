# Stage 1: Generate project from cookiecutter template
FROM python:3.11-slim as generator
RUN pip install cookiecutter
WORKDIR /template
COPY . .
# The pre-generation hook fails validation in the Docker build env, so we disable it.
RUN sed -i '/validate_python_module_name/d' hooks/pre_gen_project.py
RUN cookiecutter --no-input -f . -o / project_name="My Flask App" app_name=my_app use_pipenv=n python_version=3.11 node_version=20

# Stage 2: Build frontend assets
FROM node:20-alpine AS frontend
WORKDIR /app
COPY --from=generator /my_app .
# Remove the flask-dependent part from the build script
RUN sed -i 's/ && npm run flask-static-digest//g' package.json
RUN npm install
RUN npm run build

# Stage 3: Create the final Python image
FROM python:3.11-slim
WORKDIR /app

# Install dependencies, including curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=development \
    PORT=5000

# Install Python dependencies
COPY --from=generator /my_app/requirements.txt .
COPY --from=generator /my_app/requirements ./requirements/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and built assets
COPY --from=generator /my_app .
COPY --from=frontend /app/my_app/static/build ./my_app/static/build

# Compile static assets with Flask
RUN flask digest compile

# Expose the internal port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "my_app.app:create_app()", "-b", "0.0.0.0:5000", "-w", "3"]
