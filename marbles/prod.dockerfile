# prod.dockerfile
# Created by: Michael Cole
# Updated by: Michael Cole
# ------------------------
# Build instructions for the app
# container - to be used in production

FROM python:3.7.5-slim

LABEL maintainer="Michael Cole <mcole042891@gmail.com>"

ENV WORKDIR="/marbles"
RUN mkdir ${WORKDIR}
WORKDIR ${WORKDIR}

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . ${WORKDIR}

EXPOSE 5000

CMD gunicorn --bind ${FLASK_HOST}:${FLASK_PORT} wsgi:app

