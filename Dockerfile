FROM python:3.12-slim
# set work directory
WORKDIR /FBFlask/

# set environment variable
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /FBFlask/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /FBFlask/

VOLUME /FBFlask/static/media

EXPOSE 5000

RUN gunicorn -k eventlet -w 1 -b 127.0.0.1:5000 app:app