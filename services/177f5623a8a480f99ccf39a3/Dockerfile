FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/177f5623a8a480f99ccf39a3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p results-db

EXPOSE 5000

CMD ["python", "DecisionViualization.py"]