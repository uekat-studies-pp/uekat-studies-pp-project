ARG NODE_IMAGE_VERSION=18-alpine
FROM node:${NODE_IMAGE_VERSION}

CMD ["sh", "-c", "[ ! -d 'node_modules' ] && yarn install; yarn dev --host 0.0.0.0"]
