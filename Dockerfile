FROM python:3.9-alpine
LABEL maintainer="Paul Onyekwelu"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D app
RUN chown -R app:app /app/
RUN chown -R app:app /vol/
RUN chmod -R 755 /vol/web
USER app

# dependencies for the pillow package
# jpeg-dev
# musl-dev
# zlib
# zlib-dev