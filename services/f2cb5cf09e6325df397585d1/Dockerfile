FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV HOME=~/.hyperlpr3

WORKDIR /home/ubuntu/deploy-projects/f2cb5cf09e6325df397585d1

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libegl1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY Prj-Python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Prj-Python/ .
RUN pip install --no-cache-dir -e .

EXPOSE 8715

CMD ["lpr3", "rest", "--port", "8715", "--host", "0.0.0.0"]