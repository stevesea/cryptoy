.PHONY: help

SHELL := /bin/bash
DIR := $(strip $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))


EXECUTABLES = awk docker sops poetry
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

APP_NAME := cryptoy


docker-build: ## Build the container
	DOCKER_BUILDKIT=1 docker build -t $(APP_NAME) .

docker-run: docker-build ## run the container
	docker run --rm -it $(APP_NAME) 

dive: docker-build
	docker run --rm -it \
        -e CI="true" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        wagoodman/dive:latest $(APP_NAME)

hadolint: ## run hadolint on the Dockerfile
	-docker run --rm -i hadolint/hadolint < Dockerfile

dockle: docker-build ## run dockle on the container image
	docker run --rm -i \
        -v /var/run/docker.sock:/var/run/docker.sock \
        goodwithtech/dockle:latest -i CIS-DI-0006 -i CIS-DI-0005 $(APP_NAME)

docker-lint: hadolint dockle ## run docker image linters

install: 
	poetry install 

test: install 
	poetry run pytest

run: 
	poetry run cryptoy 