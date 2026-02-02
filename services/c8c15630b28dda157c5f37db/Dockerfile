FROM python:3.10-slim

# Install curl for healthcheck, git for HPSv2, and tkinter dependencies
RUN apt-get update && apt-get install -y curl git libtk8.6 tcl8.6 procps && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=all
ENV WORLD_SIZE=1

WORKDIR /home/ubuntu/deploy-projects/c8c15630b28dda157c5f37db

# Copy requirements and install dependencies
COPY VADER-ModelScope/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Upgrade wandb to support numpy 2.x
RUN pip install --no-cache-dir 'wandb>=0.18.0'

# Copy entire project
COPY web_server.py /home/ubuntu/deploy-projects/c8c15630b28dda157c5f37db/web_server.py
COPY . .

# Install HPSv2 for reward scoring
RUN git clone https://github.com/tgxs002/HPSv2.git && cd HPSv2 && pip install . && cd .. && rm -rf HPSv2

WORKDIR /home/ubuntu/deploy-projects/c8c15630b28dda157c5f37db/VADER-ModelScope

# Default command for training
CMD ["python", "train_t2v_lora.py"]