FROM node:20-alpine

RUN apk add --no-cache git

WORKDIR /home/ubuntu/deploy-projects/667a508cbdb1f85dd897b1dc

COPY package*.json ./
RUN npm install --omit=dev --ignore-scripts

COPY . .

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "server.js"]