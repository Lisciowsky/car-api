FROM python:3.9.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN apk update
RUN apk --update add gcc libgcc musl-dev jpeg-dev zlib-dev postgresql-dev

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN python manage.py test

ENTRYPOINT ["/home/app/entrypoint.sh"]
