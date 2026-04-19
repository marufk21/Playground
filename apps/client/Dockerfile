FROM node:20-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm
RUN pnpm install

COPY . .

# Build app
RUN pnpm build

# Serve using simple server
RUN npm install -g serve

CMD ["serve", "-s", "dist", "-l", "5173"]