FROM python:3.6

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y libkrb5-dev krb5-user

COPY . /src

WORKDIR /src

RUN pip install .
