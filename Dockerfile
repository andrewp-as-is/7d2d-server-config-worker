FROM python:3.8.2-buster

COPY ./ /code/
WORKDIR /code/

RUN apt-get update && apt-get install -y curl
RUN pip install -r /code/requirements.txt

ENTRYPOINT ["/bin/sh","/code/entrypoint.sh"]
