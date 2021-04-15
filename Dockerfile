FROM python:3.8-buster

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y cmake

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
