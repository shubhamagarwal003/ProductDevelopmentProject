# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3-onbuild

RUN apt-get update && \
    apt-get upgrade -y && \     
    apt-get install -y nginx && \ 
  echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
  chown -R www-data:www-data /var/lib/nginx

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash - && \
	apt install -y nodejs && \
	npm install -g rollup 

# COPY startup script into known file location in container

VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/home/docker/"]


COPY start.sh /home/docker/start.sh

COPY risk_management /home/docker/code/

COPY docker/nginx-app.conf /etc/nginx/sites-available/default

WORKDIR /etc/nginx
ENTRYPOINT ["/home/docker/start.sh"]

EXPOSE 80
