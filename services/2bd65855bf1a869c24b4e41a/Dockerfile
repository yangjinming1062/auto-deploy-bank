FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

RUN apt-get update && apt-get install -y \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfreetype6-dev \
    libpng-dev \
    libgomp1 \
    libtk8.6 \
    tk-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/2bd65855bf1a869c24b4e41a

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

CMD ["python", "app.py"]