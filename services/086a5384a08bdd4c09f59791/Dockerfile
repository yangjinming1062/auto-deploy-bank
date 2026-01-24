FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/086a5384a08bdd4c09f59791

COPY runtime/web/requirements.txt ./runtime/web/requirements.txt

RUN pip install --no-cache-dir -r runtime/web/requirements.txt

COPY runtime/web/ .

EXPOSE 7860

CMD ["python", "app.py"]