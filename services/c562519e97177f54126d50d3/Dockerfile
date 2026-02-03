# Multi-stage build for AI-Practices

FROM python:3.10-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

FROM base as dependencies

COPY requirements.txt pyproject.toml ./

RUN pip install --upgrade pip setuptools wheel

# Install core dependencies first
RUN pip install numpy>=1.26.0 pandas>=2.2.0 scipy>=1.14.0

# Install deep learning frameworks
RUN pip install torch>=2.5.0 torchvision>=0.20.0 torchaudio>=2.5.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install tensorflow>=2.18.0 keras>=3.8.0

# Install remaining ML and data processing libraries
RUN pip install \
    scikit-learn>=1.5.0 \
    xgboost>=2.1.0 \
    lightgbm>=4.5.0 \
    matplotlib>=3.9.0 \
    seaborn>=0.13.0 \
    plotly>=5.24.0 \
    opencv-python>=4.10.0 \
    pillow>=11.0.0 \
    tqdm>=4.67.0 \
    h5py>=3.12.0 \
    requests>=2.32.0 \
    pyyaml>=6.0.0

# Install NLP and LLM libraries
RUN pip install \
    nltk>=3.9.0 \
    transformers>=4.47.0 \
    tokenizers>=0.21.0 \
    peft>=0.14.0 \
    accelerate>=1.2.0 \
    bitsandbytes>=0.45.0 \
    sentence-transformers>=3.3.0

# Install RAG and vector databases
RUN pip install \
    langchain>=0.3.0 \
    langchain-community>=0.3.0 \
    chromadb>=0.5.0 \
    faiss-cpu>=1.9.0

# Install multimodal libraries
RUN pip install \
    diffusers>=0.32.0 \
    timm>=1.0.0 \
    librosa>=0.10.0

# Install Jupyter
RUN pip install \
    jupyter>=1.1.0 \
    notebook>=7.3.0 \
    ipywidgets>=8.1.0 \
    jupyterlab>=4.3.0

# Install dev tools
RUN pip install \
    pytest>=8.3.0 \
    pytest-cov>=6.0.0 \
    pytest-xdist>=3.6.0 \
    black>=24.10.0 \
    ruff>=0.8.0 \
    mypy>=1.13.0 \
    pre-commit>=4.0.0 \
    types-requests>=2.32.0 \
    types-pyyaml>=6.0.0

FROM dependencies as development

RUN pip install pytest pytest-cov pytest-xdist black ruff mypy pre-commit jupyter notebook

COPY . .

CMD ["bash"]

FROM dependencies as production

COPY healthcheck_server.py ./
COPY 01-foundations/ ./01-foundations/
COPY 02-neural-networks/ ./02-neural-networks/
COPY 03-computer-vision/ ./03-computer-vision/
COPY 04-sequence-models/ ./04-sequence-models/
COPY 05-advanced-topics/ ./05-advanced-topics/
COPY 06-generative-models/ ./06-generative-models/
COPY 07-reinforcement-learning/ ./07-reinforcement-learning/
COPY 08-theory-notes/ ./08-theory-notes/
COPY 09-practical-projects/ ./09-practical-projects/
COPY 10-large-language-models/ ./10-large-language-models/
COPY 11-multimodal-learning/ ./11-multimodal-learning/
COPY 12-deployment-optimization/ ./12-deployment-optimization/
COPY 13-distributed-training/ ./13-distributed-training/
COPY 14-agents-reasoning/ ./14-agents-reasoning/
COPY scripts/ ./scripts/
COPY utils/ ./utils/
COPY pyproject.toml ./

RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["python", "healthcheck_server.py"]

FROM dependencies as jupyter

RUN pip install jupyter notebook jupyterlab ipywidgets

COPY . .

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

FROM development as test

COPY test_wrapper.sh /app/test_wrapper.sh
RUN chmod +x /app/test_wrapper.sh

EXPOSE 8080

CMD ["/app/test_wrapper.sh"]