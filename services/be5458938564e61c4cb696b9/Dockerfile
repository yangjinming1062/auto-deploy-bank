FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/be5458938564e61c4cb696b9

# Install wget for healthcheck
RUN apk add --no-cache wget

# Copy build directory first (needed by postinstall)
COPY build/ ./build/

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies (skip postinstall to avoid build requirements)
RUN npm ci --ignore-scripts

# Copy source code
COPY . .

# Create startup script
RUN printf '%s\n' '#!/bin/sh' 'sed -i "s/127\.0\.0\.1/0.0.0.0/g" /home/ubuntu/deploy-projects/be5458938564e61c4cb696b9/build/simpleserver.ts' 'exec node --import tsx /home/ubuntu/deploy-projects/be5458938564e61c4cb696b9/build/simpleserver' > /start.sh && chmod +x /start.sh

# Run simpleserver on port 8080
EXPOSE 8080

CMD ["/start.sh"]