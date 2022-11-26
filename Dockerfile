FROM python:3.9-alpine
LABEL maintainer="Paul Onyekwelu"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY ./app /app

EXPOSE 8000

# RUN adduser -D app
# USER app
