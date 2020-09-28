FROM python:3.8.5-slim-buster

ENV PYTHONUNBUFFERD 1

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3-dev build-essential

RUN apt-get -y install binutils libproj-dev gdal-bin

RUN python -m pip install --upgrade pip

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /home/App
WORKDIR /home/App
COPY . /home/App

# RUN adduser -D user
# USER user