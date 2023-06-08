ARG PYTHON_IMAGE_VERSION=alpine
FROM python:${PYTHON_IMAGE_VERSION}

LABEL org.opencontainers.image.source https://github.com/uekat-studies-pp/uekat-studies-pp-project
LABEL org.opencontainers.image.description='Uniwersytet Ekonimiczny in Katowice - project for the subject "Projekt programistyczny" - Backend image'
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
COPY backend .

RUN pip install -r requirements.txt

ARG POSTGRES_USER=default
ENV POSTGRES_USER=${POSTGRES_USER}
ARG POSTGRES_PASSWORD=secret
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ARG POSTGRES_DB=default
ENV POSTGRES_DB=${POSTGRES_DB}
ARG POSTGRES_HOST=db
ENV POSTGRES_HOST=${POSTGRES_HOST}
ARG POSTGRES_PORT=5432
ENV POSTGRES_PORT=${POSTGRES_PORT}

CMD ["python", "main.py"]
