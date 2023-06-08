ARG NGINX_IMAGE_VERSION
FROM nginx:${NGINX_IMAGE_VERSION}

LABEL org.opencontainers.image.source https://github.com/uekat-studies-pp/uekat-studies-pp-project
LABEL org.opencontainers.image.description='Uniwersytet Ekonimiczny in Katowice - project for the subject "Projekt programistyczny" - Nginx image'
LABEL org.opencontainers.image.licenses=MIT

RUN apk add openssl bash

COPY docker/nginx/prod/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/prod/sites-available/ /etc/nginx/sites-available
COPY docker/nginx/prod/ssl/ /etc/nginx/ssl

ADD docker/nginx/prod/startup.sh /opt/startup.sh
RUN sed -i 's/\r//g' /opt/startup.sh
CMD ["/bin/bash", "/opt/startup.sh"]
