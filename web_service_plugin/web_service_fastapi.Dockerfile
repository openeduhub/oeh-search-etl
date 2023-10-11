FROM python:3.7-alpine as base

COPY web_service_plugin/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY web_service_plugin/ /web_service_plugin

WORKDIR /web_service_plugin

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]