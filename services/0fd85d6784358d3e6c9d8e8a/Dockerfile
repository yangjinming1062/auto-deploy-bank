FROM node:20-alpine

WORKDIR /home/node/dvba

ENV NODE_ENV=production
ENV PORT=3000

COPY BackendServer/package*.json ./
RUN npm install --only=production

COPY BackendServer/. .

EXPOSE 3000

CMD ["node", "bin/www"]