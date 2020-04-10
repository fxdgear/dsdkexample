FROM quay.io/pennsignals/alpine-3.8-python-3.7-machinelearning-mssql:7.0
WORKDIR /tmp
COPY ./README.md .
COPY ./setup.cfg .
COPY ./setup.py .
COPY ./.git ./.git
COPY ./local ./local
COPY ./src ./src
COPY ./tests ./tests
COPY ./CHANGELOG.md .
RUN apk add --no-cache --virtual .build git
RUN pip install --quiet --no-cache-dir "."
RUN apk del --no-cache .build
