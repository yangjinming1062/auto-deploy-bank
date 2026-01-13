# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y build-essential curl ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Pre-download the models
RUN mkdir -p asset config && \
    curl -L -o asset/DVAE.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/DVAE.pt && \
    curl -L -o asset/Decoder.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/Decoder.pt && \
    curl -L -o asset/GPT.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/GPT.pt && \
    curl -L -o asset/Vocos.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/Vocos.pt && \
    curl -L -o asset/spk_stat.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/spk_stat.pt && \
    curl -L -o asset/tokenizer.pt https://huggingface.co/2Noise/ChatTTS/resolve/main/asset/tokenizer.pt && \
    curl -L -o config/decoder.yaml https://huggingface.co/2Noise/ChatTTS/resolve/main/config/decoder.yaml && \
    curl -L -o config/dvae.yaml https://huggingface.co/2Noise/ChatTTS/resolve/main/config/dvae.yaml && \
    curl -L -o config/gpt.yaml https://huggingface.co/2Noise/ChatTTS/resolve/main/config/gpt.yaml && \
    curl -L -o config/path.yaml https://huggingface.co/2Noise/ChatTTS/resolve/main/config/path.yaml && \
    curl -L -o config/vocos.yaml https://huggingface.co/2Noise/ChatTTS/resolve/main/config/vocos.yaml

# Set environment variables
ENV PYTORCH_ENABLE_MPS_FALLBACK=1
ENV HF_HOME=~/.cache/huggingface
ENV PYTHONUNBUFFERED=1

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define the command to run on container start
CMD ["python", "examples/web/webui.py"]
