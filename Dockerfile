FROM python:3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    TINI_VERSION=0.19.0

RUN \
    apt-get -yqq update \
    && apt-get install --no-install-suggests --no-install-recommends --yes \
    gcc \
    g++ \
    libffi-dev \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/* 
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /tini
RUN chmod +x /tini

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.4

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --no-dev --no-root

COPY . .
RUN . /venv/bin/activate && poetry build

FROM base as final

COPY --from=builder /venv /venv
COPY --from=builder /app/dist .

RUN . /venv/bin/activate && pip install *.whl
ENTRYPOINT [ "/tini", "-e", "143", "--" ]
CMD ["/venv/bin/cryptoy"]