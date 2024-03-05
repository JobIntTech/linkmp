FROM python:3.12.0-alpine
MAINTAINER Guido Navalesi <guido@jobint.com>

COPY MP.py /opt/MP.py

WORKDIR /opt

RUN pip install flask
RUN pip install mercadopago
RUN pip install requests
RUN pip install itsdangerous


CMD ["/bin/sh", "-c", "python /opt/MP.py"]