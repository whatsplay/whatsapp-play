FROM python:3.6-alpine
#LABEL MAINTAINER

# Copying files
COPY wplay/ /whatsapp-play/wplay
COPY setup.py /whatsapp-play/setup.py
COPY README.md /whatsapp-play/README.md
COPY requirements.txt /whatsapp-play/requirements.txt

# Dependencies
WORKDIR /whatsapp-play
RUN apk add build-base
RUN apk add make
RUN apk add gcc musl-dev libffi-dev openssl-dev
RUN pip install cryptography
RUN apk add --no-cache libffi-dev build-base py3-pip python3-dev && pip install cffi
RUN pip install -r requirements.txt

ENTRYPOINT echo "Hello, welcome to whatsapp-play"
ENTRYPOINT ["python3 -m wplay -h"]

CMD [ "python"]