# syntax=docker/dockerfile:1.4

ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim as app
ARG POETRY_VERSION=1.6.1
ARG POETRY_ARGS="--without dev"
ENV POETRY_HOME=/opt/poetry\
    PATH="${PATH}:/opt/poetry/bin"
RUN python3 -m venv ${POETRY_HOME} &&\
    ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION} &&\
    poetry config virtualenvs.create false
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN poetry check && poetry check --lock
RUN poetry install ${POETRY_ARGS}
COPY ./bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]