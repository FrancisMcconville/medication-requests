FROM python:3.10-slim AS compile
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

ARG PIP_CONF_PATH=/run/secrets/pip.conf
ENV PIP_CONFIG_FILE=$PIP_CONF_PATH

WORKDIR /service

COPY requirements.txt .

RUN --mount=type=secret,id=pip.conf,dst=$PIP_CONF_PATH \
    pip install --no-cache-dir --upgrade pip \
    && pip install virtualenv \
    && python3 -m virtualenv .venv \
    && . .venv/bin/activate \
    && pip install -r requirements.txt

RUN useradd --create-home tech-test
USER tech-test

WORKDIR /service
ENV PYTHONPATH=. \
    PATH="/service/.venv/bin:$PATH"

COPY --chown=tech-test src ./src
