FROM python:3.7-alpine

ENV HOME_DIR /webscraping2
WORKDIR $HOME_DIR

COPY . $HOME_DIR

RUN pip install -r requirements.txt

