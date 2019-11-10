FROM python:3.6-alpine

ADD wplay/ /whatsapp-play/wplay
ADD setup.py /whatsapp-play/setup.py
ADD README.md /whatsapp-play/README.md

WORKDIR /whatsapp-play
RUN pip install .

ENTRYPOINT echo "Hello, welcome to whatsapp-play"
