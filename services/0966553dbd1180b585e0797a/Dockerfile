# Use conda base image for pre-built scientific packages
FROM continuumio/miniconda3:latest

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SERVER_HOST=0.0.0.0

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/0966553dbd1180b585e0797a

# Create conda environment and install dependencies
# Using conda for pre-built binaries of scientific packages
RUN /bin/bash -c "conda create -n flaskapp python=3.9 -y && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate flaskapp && \
    conda install -c conda-forge numpy=1.24 pandas=1.5 prophet=1.1 -y && \
    conda install -c conda-forge matplotlib=3.6 scipy=1.10 -y && \
    pip install --no-cache-dir Flask==2.3.2 yfinance==0.1.54 Pillow==9.3.0 plotly==4.9.0 && \
    pip install --no-cache-dir tensorflow-cpu==2.12.0 && \
    pip install --no-cache-dir SQLAlchemy==1.3.18 protobuf==3.18.3 requests==2.31.0 urllib3==1.26.5 && \
    pip install --no-cache-dir tensorboard==2.12.0 tensorboard-plugin-wit==1.8.1 tensorflow-estimator==2.12.0 && \
    conda clean -afy"

# Copy application code
COPY . .

# Expose internal port
EXPOSE 5555

# Run the Flask application with conda environment activated
CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate flaskapp && python runserver.py"]