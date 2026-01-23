FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/e92c55559356cb9a9b6438ad

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["python", "start_app.py"]