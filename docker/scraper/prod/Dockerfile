ARG PYTHON_IMAGE_VERSION=alpine
FROM python:${PYTHON_IMAGE_VERSION}

LABEL org.opencontainers.image.source https://github.com/uekat-studies-pp/uekat-studies-pp-project
LABEL org.opencontainers.image.description='Uniwersytet Ekonimiczny in Katowice - project for the subject "Projekt programistyczny" - Scraper image'
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /app
COPY scraper .

RUN pip install -r requirements.txt

CMD ["python cron.py"]
