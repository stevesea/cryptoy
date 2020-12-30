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

WORKDIR /app

#####
# copy just the poetry toml/lock, and install 3rd party deps
FROM base as builder-deps

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    python3 -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    . /venv/bin/activate && poetry install --no-dev --no-root

#####
# copy the source and build / install a wheel
FROM builder-deps as builder-app

COPY . .
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    . /venv/bin/activate && poetry build && pip install --no-cache-dir dist/*.whl


#####
FROM base as final
USER nobody
COPY --from=builder-app --chown=nobody:nobody /venv /venv
ENTRYPOINT [ "/tini", "-e", "143", "--" ]
CMD ["/venv/bin/cryptoy"]