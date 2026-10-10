FROM python:3.9-buster

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python modules
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# copy project tree;
# coment this out for debug if you want to run code that lies outside of container and don't forget also change the .yml file
#COPY ./lab3 .

#CMD ["python", "cli.py"]
