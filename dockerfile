FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=0
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY app/ .
CMD ["python3", "-u", "./main.py"]