# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3-onbuild

RUN apt-get update && \
    apt-get upgrade -y && \     
    apt-get install -y \
    nginx

# COPY startup script into known file location in container
COPY start.sh /start.sh

COPY risk_management /home/docker/code/

COPY docker/nginx-app.conf /etc/nginx/sites-available/default
# EXPOSE port 8000 to allow communication to/from server

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
CMD ["/start.sh"]
CMD ["while true; do sleep 1000; done"]


# CMD specifcies the command to execute to start the server running.
# done!
# 
# 
# 