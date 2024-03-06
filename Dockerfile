FROM python:3.12.0-alpine
MAINTAINER Guido Navalesi <guido@jobint.com>

COPY app.py /opt/app.py

WORKDIR /opt

RUN pip install flask
RUN pip install mercadopago
RUN pip install itsdangerous
RUN pip install requests

CMD ["/bin/sh", "-c", "python /opt/app.py"]