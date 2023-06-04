ARG RUST_IMAGE_VERSION=alpine
FROM rust:${RUST_IMAGE_VERSION}

CMD ["sh", "-c", "cargo install --path . && cron-app"]
