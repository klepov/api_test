FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY api_nginx.conf /etc/nginx/sites-available/


RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/api_nginx.conf /etc/nginx/sites-enabled/

