FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
COPY lib_agent.py lib_agent.py
COPY lib_model.py lib_model.py
COPY lib_sections.py lib_sections.py
COPY lib_simulation.py lib_simulation.py
COPY server.py server.py
COPY data data
COPY static static
COPY downloads downloads
COPY uploads uploads

RUN pip3 install -r requirements.txt
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT ["python3", "-m", "flask", "run"]