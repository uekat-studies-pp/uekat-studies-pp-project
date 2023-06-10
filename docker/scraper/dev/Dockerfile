ARG PYTHON_IMAGE_VERSION=alpine
FROM python:${PYTHON_IMAGE_VERSION}

RUN crontab -l | { cat; echo "0 * * * * python /app/main.py"; } | crontab -

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

COPY scraper/requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
COPY scraper/main.py main.py
CMD ["python", "main.py"]
#CMD ["crond"]
