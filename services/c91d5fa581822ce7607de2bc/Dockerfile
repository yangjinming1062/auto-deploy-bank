# Use a slim Python base image
FROM python:3.9-slim-buster

# Install build tools, git, and curl
RUN sed -i -e 's/deb.debian.org/archive.debian.org/g' -e '/buster-updates/d' /etc/apt/sources.list && apt-get update && apt-get install -y build-essential curl git libblas-dev liblapack-dev gfortran zlib1g-dev libjpeg-dev libopenblas-dev python3-scipy python3-pandas python3-sklearn && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PARLAI_DATAPATH=/app/data
ENV PYTHONPATH=/app:/app/parlai

# Create the data directory
RUN mkdir -p $PARLAI_DATAPATH

# Copy requirements and install dependencies
COPY requirements.txt .

# Install build dependencies first, in separate layers for better debugging
RUN pip install "pip<24"
RUN pip install "setuptools<58"
RUN pip install "Cython<3" "numpy==1.17.5"
RUN pip install "torch>=1.4.0" "torchtext>=0.5.0"

# Create a filtered requirements file, also excluding pandas and scipy
RUN grep -v -e "scipy" -e "torch" -e "numpy" -e "Cython" -e "setuptools" -e "pip" -e "pandas" -e "scikit-learn" requirements.txt > requirements_filtered.txt


# Install tokenizers to avoid dependency resolution loop
RUN pip install "tokenizers==0.10.3"

# Install the rest of the requirements
RUN CFLAGS="-Wno-error" pip install --no-cache-dir --no-build-isolation -r requirements_filtered.txt
RUN pip install "typing-extensions>=3.10.0.0"

# Copy the rest of the application code
COPY . .

# Overwrite the original requirements file with the filtered one
RUN mv requirements_filtered.txt requirements.txt

# Install the ParlAI project
RUN python setup.py install

# Expose the internal port
EXPOSE 35496

CMD ["python", "-m", "parlai.scripts.interactive_web", "-mf", "zoo:blender/blender_90M/model", "-t", "parlai.agents.local_human.local_human:LocalHumanAgent", "--port", "35496", "--host", "0.0.0.0"]