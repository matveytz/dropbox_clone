# pull official base image
FROM python:3.10.12-slim-buster

# set work directory
RUN mkdir /dropbox_clone
WORKDIR /dropbox_clone

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod a+x docker/*.sh

# CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]