FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt /backend

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /backend/



