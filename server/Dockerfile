FROM python:3.6.2
RUN apt update
RUN apt install -y python3-pip binutils libproj-dev gdal-bin
ENV PYTHONUNBUFFERED 1
RUN mkdir /var/log/uwsgi
RUN mkdir /docker_api
COPY . /docker_api
WORKDIR /docker_api
RUN pip3 install -r requirements.txt



