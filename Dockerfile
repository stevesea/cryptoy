# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * Update pip to support bdist_wheel
FROM python:3.9-slim-buster AS build
RUN apt-get -yqq update && \
    apt-get install --no-install-suggests --no-install-recommends --yes \
    python3-pip \
    python3-venv \
    && python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN /venv/bin/poetry install --no-root
ENV \
    TINI_VERSION=0.19.0
ADD https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini-static /tini

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian10
COPY --from=build-venv /venv /venv
COPY --from=build-venv /tini /tini
COPY . /app
WORKDIR /app
RUN /venv/bin/poetry install 
ENTRYPOINT [ "/tini", "-e", "143", "--" ]
CMD ["/venv/bin/python3", "cryptoy"]

