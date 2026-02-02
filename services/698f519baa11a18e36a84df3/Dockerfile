FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/698f519baa11a18e36a84df3

WORKDIR /home/ubuntu/deploy-projects/698f519baa11a18e36a84df3

RUN apt-get update && apt-get install -y curl net-tools && rm -rf /var/lib/apt/lists/*

COPY training/requirements.txt .
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir 'flask>=2.3.0' 'numpy<2.0' 'torch>=1.11.0' 'redis>=4.3.0' 'wandb>=0.12.0' \
    'matplotlib>=3.5.0' 'msgpack>=1.0.0' 'msgpack-numpy>=0.4.7' \
    'gym>=0.24.0' 'scipy>=1.7.0' 'pygame>=2.1.0' 'numba>=0.55.0' \
    'trueskill>=0.4.0' 'tqdm>=4.56.0' 'plotly>=5.8.0' 'pillow>=9.0.0' \
    'EARL-pytorch>=0.5.0' 'rlgym-tools>=2.0.0' 'keyboard>=0.13.0' \
    'rlbot>=1.0'

COPY . .

CMD ["python", "run.py"]