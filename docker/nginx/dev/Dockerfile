ARG NGINX_IMAGE_VERSION
FROM nginx:${NGINX_IMAGE_VERSION}

RUN apk add openssl bash

ADD ./startup.sh /opt/startup.sh
RUN sed -i 's/\r//g' /opt/startup.sh
CMD ["/bin/bash", "/opt/startup.sh"]
