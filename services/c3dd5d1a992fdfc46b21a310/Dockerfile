FROM python:3.8-slim

RUN apt-get update && apt-get install -y curl thrift-compiler && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LUCIDAROOT=/app
ENV PYTHONPATH=/app/lucida:$PYTHONPATH

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY lucida /app/lucida
COPY tools /app/tools

# Generate Thrift Python files
RUN mkdir -p /app/lucida/lucidatypes && \
    mkdir -p /app/lucida/lucidaservice && \
    thrift -gen py -out /app/lucida/ /app/lucida/lucidatypes.thrift && \
    thrift -gen py -out /app/lucida/ /app/lucida/lucidaservice.thrift && \
    # Fix import paths in generated files
    find /app/lucida/lucidaservice -name "*.py" -exec sed -i 's/import lucidatypes/import lucida.lucidatypes/g' {} \; && \
    find /app/lucida/lucidaservice -name "*.py" -exec sed -i 's/from lucidatypes/from lucida.lucidatypes/g' {} \; && \
    find /app/lucida/lucidaservice -name "*.py" -exec sed -i 's/\([^a-zA-Z0-9_]\)lucidatypes\./\1lucida.lucidatypes./g' {} \; && \
    find /app/lucida/lucidaservice -name "*.py" -exec sed -i 's/^lucidatypes\./lucida.lucidatypes./g' {} \; && \
    find /app/lucida/lucidaservice -name "*.py" -exec sed -i 's/lucida\.lucida\./lucida./g' {} \;

# Fix Python 2 to 3 compatibility in source code
RUN find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/\r$//' {} \; && \
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/print \([^(].*\)/print(\1)/g' {} \; && \
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/@tornado.web.asynchronous/@tornado.web.gen.coroutine/g' {} \; && \
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/from Parser import cmd_port/from .Parser import cmd_port/g' {} \; && \
    # Fix module paths to use lucida package
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/from controllers\./from lucida.commandcenter.controllers./g' {} \; && \
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/import controllers\./import lucida.commandcenter.controllers./g' {} \;

# Fix Parser.py for configparser
RUN sed -i 's/from configparser import SafeConfigParser/from configparser import ConfigParser as SafeConfigParser/' /app/lucida/commandcenter/controllers/Parser.py

# Fix any incomplete print statements
RUN find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i 's/print("\([^"]*\)";$/print("\1")/g' {} \; && \
    find /app/lucida/commandcenter -name "*.py" -type f -exec sed -i "s/print('\''\([^'\'']*\)'\'';$/print('\''\1'\'')/g" {} \;

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["python", "lucida/commandcenter/app.py"]