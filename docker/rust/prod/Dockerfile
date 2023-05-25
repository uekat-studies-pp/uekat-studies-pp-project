ARG RUST_IMAGE_VERSION=alpine
FROM rust:${RUST_IMAGE_VERSION}

WORKDIR /app
COPY backend .

RUN cargo install --path .

CMD ["backend"]
