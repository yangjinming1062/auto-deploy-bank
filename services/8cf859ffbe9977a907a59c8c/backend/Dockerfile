# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV ALLOWED_HOSTS=*

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

FROM base AS prod

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
