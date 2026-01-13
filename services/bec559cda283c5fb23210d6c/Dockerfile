FROM python:3.8-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y curl nodejs npm && rm -rf /var/lib/apt/lists/*
COPY . .
RUN npm install --prefix ./example
RUN sed -i '4d' example/requirements.txt
RUN pip install --no-cache-dir -r example/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app"
RUN python example/manage.py migrate
RUN python example/manage.py collectstatic --no-input
CMD ["python", "example/manage.py", "runserver", "0.0.0.0:8000"]