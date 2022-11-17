FROM python:3.7-slim-bullseye
COPY requirements.txt /tmp/
RUN pip install -U pip && pip install -r /tmp/requirements.txt
WORKDIR /app/
