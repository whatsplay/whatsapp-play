FROM ubuntu:18.04
FROM python:3.6

#LABEL MAINTAINER

RUN apt-get update && apt-get upgrade -y
# Dependencies
RUN apt-get install -y python3.6 python-dev python-pip python-virtualenv

# Copying files
COPY wplay/ /whatsapp-play/wplay
COPY setup.py /whatsapp-play/setup.py
COPY README.md /whatsapp-play/README.md
COPY requirements.txt /whatsapp-play/requirements.txt

# Create virtualenv with requirements
RUN virtualenv venv && /./venv/bin/pip install -r requirements.txt


WORKDIR /whatsapp-play

ENTRYPOINT echo "Hello, welcome to whatsapp-play"
ENTRYPOINT ["python3 -m wplay -h"]

CMD [ "python"]