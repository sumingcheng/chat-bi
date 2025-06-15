FROM node:20.10.0-alpine AS builder

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm && pnpm install --frozen-lockfile && pnpm store prune

COPY . ./

RUN pnpm run build

FROM nginx:stable-alpine AS production

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=builder /app/dist ./

EXPOSE 30001

CMD ["nginx", "-g", "daemon off;"]
