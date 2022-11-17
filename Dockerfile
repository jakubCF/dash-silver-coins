FROM python:3.8-slim-bullseye
COPY requirements.txt /tmp/
RUN pip install -U pip && pip install -r /tmp/requirements.txt
WORKDIR /app/
