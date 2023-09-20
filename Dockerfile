FROM python:3.10

WORKDIR /app/src
ADD src /app/src
ADD assets /app/assets

RUN pip install -r requirements.txt; \
    pip install gunicorn


CMD gunicorn -w 1 --bind 0.0.0.0:8080 --access-logfile '-' app:app