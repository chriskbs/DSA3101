FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT ["python3", "-m", "flask", "run"]