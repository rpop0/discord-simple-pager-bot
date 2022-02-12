FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY . .

RUN apt-get update && apt-get install build-essential -y

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]