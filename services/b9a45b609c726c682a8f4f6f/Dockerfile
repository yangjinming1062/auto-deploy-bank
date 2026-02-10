FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/b9a45b609c726c682a8f4f6f

RUN apk add --no-cache curl

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["node", "server.js"]