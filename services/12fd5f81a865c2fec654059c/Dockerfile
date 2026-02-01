FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl libhdf5-dev libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/12fd5f81a865c2fec654059c

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-deps -e .

CMD ["python", "webapp.py"]