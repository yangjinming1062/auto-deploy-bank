FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/30485f8c98f8865a2d2c794c

ENV NODE_ENV=production
ENV PORT=3000

COPY package*.json ./
RUN npm install --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]