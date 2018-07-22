FROM python:2.7-alpine
COPY ./web-api /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r ./requirements.txt
CMD ["python","app.py"]
