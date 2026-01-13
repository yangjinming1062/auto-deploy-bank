FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /home/ubuntu/deploy-projects/b1c454b0aaec741a32915bbb

# Install curl for healthcheck and libraries required by OpenCV and torchvision
RUN apt-get update && apt-get install -y curl libglib2.0-0 libgl1 libjpeg-dev libpng-dev libgtk-3-0 libsm6 libxext6 libxrender-dev libgomp1 build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .

# Install PyTorch and other dependencies
RUN pip install --no-cache-dir torch torchvision

# Install remaining dependencies (remove torch entries from requirements to avoid duplicates)
RUN sed -i '/^torch/d;/^torchvision/d' requirements.txt && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 6688

# Start the Gradio demo with aggressive memory optimization
# Disabling LLaVA (--no_llava) as it requires significant GPU memory
# Using lightning model for faster inference and lower memory
CMD ["python", "gradio_demo.py", "--ip", "0.0.0.0", "--port", "6688", "--opt", "options/SUPIR_v0_Juggernautv9_lightning.yaml", "--loading_half_params", "--use_tile_vae", "--no_llava"]