FROM python:3.9.2-alpine3.12
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache gcc
RUN apk add --no-cache python3-dev
RUN apk add musl-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN adduser \
    --disabled-password \
    --no-create-home \
    "YOUR_USER"
USER YOUR_USER

ENTRYPOINT ["python3", "/main.py"]
