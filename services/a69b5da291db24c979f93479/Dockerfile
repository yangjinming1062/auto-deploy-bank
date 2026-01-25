FROM node:20-alpine

WORKDIR /home/node/app

ENV NODE_ENV=production
ENV PORT=5000

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 5000

CMD ["npm", "run", "start"]
