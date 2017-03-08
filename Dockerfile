FROM ubuntu:14.04

ENV DJANGO_PRODUCTION=true

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

# 8000 = gunicorn
EXPOSE 8000