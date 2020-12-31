# syntax = docker/dockerfile:experimental

FROM python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    TINI_VERSION=0.19.0

RUN \
    apt-get -yqq update \
    && apt-get install --no-install-suggests --no-install-recommends --yes \
    libsodium23 \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/* 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /tini
RUN chmod +x /tini


#####
# copy just the poetry toml/lock, and install 3rd party deps
FROM base as builder-deps

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.1.4

RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN python3 -m venv /venv

WORKDIR /app

COPY pyproject.toml poetry.lock ./
# use `poetry export` instead of `poetry install --no-dev --no-root`,
# this Dockerfile step is all about 3rd party dependencies, and 
# we don't want to re-run it if we just update metadata in pyproject.toml
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

#####
# copy the source and build / install a wheel
FROM builder-deps as builder-app

COPY . .
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    poetry build && /venv/bin/pip install --no-cache-dir dist/*.whl


#####
FROM base as final
USER nobody
COPY --from=builder-app --chown=nobody:nobody /venv /venv
WORKDIR /venv/bin
ENTRYPOINT [ "/tini", "-e", "143", "--" ]
CMD ["/venv/bin/python", "/venv/bin/cryptoy"]