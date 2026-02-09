FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU version
RUN pip install --no-cache-dir torch==2.2.0 torchvision==0.17.0 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
# Remove torch from requirements since we install specific version
RUN grep -v "^torch$" requirements.txt > requirements_no_torch.txt
RUN pip install --no-cache-dir -r requirements_no_torch.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "image_embedding:app", "--host", "0.0.0.0", "--port", "8001"]