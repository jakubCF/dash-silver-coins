FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY requirements.txt /tmp/
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt
WORKDIR /app/
ENV NGINX_WORKER_PROCESSES auto