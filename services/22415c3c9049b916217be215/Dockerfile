FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome for Testing (full Chrome for Selenium)
RUN CHROME_MAJOR_VERSION=$(curl -sL "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE" | head -1) \
    && echo "Chrome version: $CHROME_MAJOR_VERSION" \
    && curl -sL "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_MAJOR_VERSION}/linux64/chrome-linux64.zip" -o /tmp/chrome.zip \
    && unzip -q /tmp/chrome.zip -d /opt \
    && mv /opt/chrome-linux64 /opt/chrome \
    && ln -sf /opt/chrome/chrome /usr/local/bin/chrome \
    && rm -rf /tmp/chrome.zip

# Install ChromeDriver
RUN CHROME_MAJOR_VERSION=$(curl -sL "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE" | head -1) \
    && curl -sL "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_MAJOR_VERSION}/linux64/chromedriver-linux64.zip" -o /tmp/chromedriver.zip \
    && unzip -q /tmp/chromedriver.zip -d /tmp \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver* /tmp/chrome_version

ENV PYTHONUNBUFFERED=1
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
ENV CHROME_BIN=/usr/local/bin/chrome

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Run the application with web server
CMD ["/bin/bash", "entrypoint.sh"]