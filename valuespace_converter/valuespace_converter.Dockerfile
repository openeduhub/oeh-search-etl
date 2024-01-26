FROM python:3.11.6-alpine as base

COPY app/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app

WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]