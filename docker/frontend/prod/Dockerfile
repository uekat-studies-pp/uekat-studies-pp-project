ARG NODE_IMAGE_VERSION=18-alpine
FROM node:${NODE_IMAGE_VERSION}

LABEL org.opencontainers.image.source https://github.com/uekat-studies-pp/uekat-studies-pp-project
LABEL org.opencontainers.image.description='Uniwersytet Ekonimiczny in Katowice - project for the subject "Projekt programistyczny" - Frontend image'
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app

COPY frontend .

RUN yarn install
RUN yarn build

CMD ["node", "dist/main"]
