ARG NODE_IMAGE_VERSION=18-alpine
FROM node:${NODE_IMAGE_VERSION}

WORKDIR /app

COPY frontend .

RUN yarn install
RUN yarn build

CMD ["node", "dist/main"]
