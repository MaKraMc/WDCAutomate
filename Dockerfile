FROM python:3.12-alpine

RUN apk update

#Set timezone to Europe/London, same as on wdc
ENV TZ=Europe/London

#Install required packages
RUN apk add --no-cache firefox
RUN apk add --no-cache tesseract-ocr
RUN apk add --no-cache tesseract-ocr-data-eng
#Zlib is required for armv7
RUN apk add zlib-dev

#Copy the code
WORKDIR /app
COPY . /app

#Install the python requirements
RUN pip3 install -r /app/requirements.txt

#Make sure the startup script is executable
RUN chmod +x /app/startup.sh

CMD "/app/startup.sh"
