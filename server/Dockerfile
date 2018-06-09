FROM python:3.6.2
RUN apt update
RUN apt install -y python3-pip binutils libproj-dev gdal-bin

ENV PYTHONUNBUFFERED 1

RUN mkdir /var/log/uwsgi
RUN mkdir /docker_api
COPY . /docker_api
WORKDIR /docker_api
RUN pip3 install -r requirements.txt
CMD python manage.py collectstatic --no-input;python manage.py migrate;
CMD echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python3 manage.py shell
RUN mkdir /uwsgi
COPY ./uwsgi.ini /uwsgi
WORKDIR /uwsgi



