FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/b3b55dafb318fea698231fb5

COPY package*.json ./
RUN npm install

COPY . .

RUN npx tsc

ENV NODE_ENV=production
ENV PORT=43927

CMD ["node", "dist/server.js"]