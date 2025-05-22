FROM python:3.13.3-bookworm


WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

