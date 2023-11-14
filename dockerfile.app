ARG DATA_SOURCE

FROM python:3.12.0-slim AS base

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY gps_replay gps_replay
RUN mkdir app
COPY app/__init__.py app/__init__.py
COPY app/config.py app/config.py

FROM base AS rest_build
COPY app/main_rest.py app/main.py

FROM base as pub_sub_build
COPY app/main_reactive.py app/main.py

FROM ${DATA_SOURCE}_build AS final
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
CMD ["streamlit", "run", "--server.port", "8501", "app/main.py"]
