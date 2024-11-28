FROM python:3.12-alpine

# set work directory
WORKDIR /FBFlask/

# set environment variable
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /FBFlask/requirements.txt
RUN pip install -r requirements.txt

# create log directory
RUN mkdir -p /var/log/logApp && chmod -R 755 /var/log/logApp

# copy project
COPY . /FBFlask/

EXPOSE 5000

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "--access-logfile", "/var/log/appLog/access.log", "--error-logfile", "/var/log/appLog/error.log", "app:app"]
