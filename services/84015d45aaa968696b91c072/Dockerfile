# Builder stage
FROM node:20-alpine AS builder
ARG NEXT_PUBLIC_AGIXT_SERVER
ENV NEXT_PUBLIC_AGIXT_SERVER=$NEXT_PUBLIC_AGIXT_SERVER
WORKDIR /app
COPY package*.json ./
RUN apk add --no-cache python3 make g++ linux-headers eudev-dev && npm install
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3437
COPY --from=builder /app/package*.json ./
RUN apk add --no-cache python3 make g++ linux-headers eudev-dev && npm install --only=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/next.config.js ./
EXPOSE 3437
CMD ["npm", "start"]
