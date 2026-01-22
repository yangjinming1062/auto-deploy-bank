FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl libgl1 libxcb1 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 libxrender1 libxshmfence1 libxext6 libxcb-shm0 libxcb-dri2-0 libxcb-dri3-0 libxcb-present0 libxfixes3 libxcb-xfixes0 libxcb-glx0 libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2 libfontconfig1 libfreetype6 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/12f05413b563fe70cbed49dc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir flask gunicorn

COPY . .

RUN pip install -e .

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120"]