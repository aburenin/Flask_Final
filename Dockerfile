FROM python:3.12-alpine
# set work directory
WORKDIR /FBFlask/

# set environment variable
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /FBFlask/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /FBFlask/

EXPOSE 5000

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
