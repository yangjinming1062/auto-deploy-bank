FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/6d515aa18620039d9e77b3fa

COPY package*.json ./

RUN npm ci --only=production

COPY . .

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["node", "server.js"]