# Builder stage
FROM node:20 AS builder

WORKDIR /home/ubuntu/deploy-projects/ac1650d78b91470f594f29be

COPY package*.json ./
RUN rm -f package-lock.json && \
    rm -rf node_modules && \
    npm install

COPY . .
RUN npm run build

# Production stage
FROM node:20

WORKDIR /home/ubuntu/deploy-projects/ac1650d78b91470f594f29be

COPY --from=builder /home/ubuntu/deploy-projects/ac1650d78b91470f594f29be/package*.json ./
COPY --from=builder /home/ubuntu/deploy-projects/ac1650d78b91470f594f29be/build ./build

ENV NODE_ENV=production
ENV PORT=3000

RUN npm ci --only=production && npm install express

# Create a simple server to demonstrate the library
RUN echo 'const express = require("express"); \
const asn1 = require("./build/index.js"); \
const app = express(); \
app.get("/", (req, res) => { \
  res.json({ name: "asn1js", status: "running", library: "loaded" }); \
}); \
app.listen(3000, "0.0.0.0", () => { \
  console.log("Server running on port 3000"); \
});' > server.js

EXPOSE 3000

CMD ["node", "server.js"]