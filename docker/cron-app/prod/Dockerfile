ARG RUST_IMAGE_VERSION=alpine
FROM rust:${RUST_IMAGE_VERSION}

LABEL org.opencontainers.image.source https://github.com/uekat-studies-pp/uekat-studies-pp-project
LABEL org.opencontainers.image.description='Uniwersytet Ekonimiczny in Katowice - project for the subject "Projekt programistyczny" - Cron app image'
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
COPY scrapper .

RUN cargo install --path .

CMD ["scrapper"]
