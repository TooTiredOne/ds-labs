FROM python:3.8-alpine

RUN pip3 install flask

WORKDIR /app

COPY ./ /app

EXPOSE 8080

CMD python3 app.py