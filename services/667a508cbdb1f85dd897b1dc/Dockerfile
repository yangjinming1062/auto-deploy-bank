FROM node:20-alpine

WORKDIR /home/ubuntu/deploy-projects/667a508cbdb1f85dd897b1dc

RUN apk add --no-cache git

COPY package*.json ./
RUN npm install --omit=dev --ignore-scripts

COPY lib ./lib
COPY dist ./dist
COPY server.js ./

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["node", "server.js"]