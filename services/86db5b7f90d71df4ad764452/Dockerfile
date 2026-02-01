FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "--server.port", "8080", "--server.address", "0.0.0.0", "streamlit_app.py"]