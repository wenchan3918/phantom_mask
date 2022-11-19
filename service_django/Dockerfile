FROM python:3.9-slim-buster

RUN set -ex && mkdir /app
WORKDIR /app
ENV PIPENV_IGNORE_VIRTUALENVS=1

RUN apt-get update \
    && apt-get -y install libpq-dev build-essential lsof libmagic-dev python-psycopg2 wget \
    && apt-get clean \
    && pip install --upgrade pip \
    && pip install pipenv psycopg2-binary --no-cache-dir \

    #時區設定，台灣時區
    && rm /etc/localtime \
    && ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime


COPY ./phantom_mask/requirements.txt requirements.txt
RUN pip install -r requirements.txt

