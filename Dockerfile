FROM python:3.12.0-alpine
MAINTAINER Guido Navalesi <guido@jobint.com>

COPY app.py /opt/app.py
COPY app.py /opt/bq.py
COPY templates /opt/templates

WORKDIR /opt

RUN pip install flask
RUN pip install mercadopago
RUN pip install itsdangerous
RUN pip install requests
RUN pip install simple-salesforce
RUN pip install google-cloud-bigquery


CMD ["/bin/sh", "-c", "python /opt/app.py"]
