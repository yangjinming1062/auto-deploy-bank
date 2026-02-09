FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Build-n-Deploy-Flask-App-with-Waypoint/requirements.txt .
RUN pip install --no-cache-dir "numpy<2.0" "Jinja2<3.0" "Werkzeug<2.0" "markupsafe<2.1" "itsdangerous<2.0" && pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY Build-n-Deploy-Flask-App-with-Waypoint/app/ .

EXPOSE 5000

CMD ["python", "app.py"]