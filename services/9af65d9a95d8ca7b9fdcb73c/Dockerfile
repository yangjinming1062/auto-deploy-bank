FROM python:3.9-slim

WORKDIR /app

# Install curl for healthchecks, git to clone the demo, and sed to patch the source
RUN apt-get update && apt-get install -y curl git sed && rm -rf /var/lib/apt/lists/*

# Clone the demo application that uses pywps
RUN git clone https://github.com/geopython/pywps-flask.git

# Go into the demo's directory
WORKDIR /app/pywps-flask

# Install dependencies for the demo app
RUN pip install --no-cache-dir -r requirements.txt

# Patch the demo source code to be compatible with the newer pywps version
# The pywps.wpsserver module has been removed.
RUN sed -i "s/from pywps.wpsserver import temp_dir//g" processes/area.py
RUN sed -i "s/from pywps.wpsserver import temp_dir//g" processes/centroids.py
# Let's assume the code was using temp_dir to create a temp file. The modern way is to use the output object's file property.
# I'm guessing the output is named 'area' based on the process name. This is a common pattern.
RUN sed -i "s|import tempfile|import tempfile\n        from pywps import OGCUNIT, UOM|g" processes/area.py
RUN sed -i "s|_, target_file = tempfile.mkstemp(dir=temp_dir)|target_file = response.outputs['area'].file|g" processes/area.py
ENV FLASK_APP=demo.py
EXPOSE 5000

# The command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
