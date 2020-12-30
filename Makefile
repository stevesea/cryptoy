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

docker-run: ## run the container
	docker run --rm -it $(APP_NAME) 

docker-up: docker-build docker-run ## build & run

dive: docker-build
	docker run --rm -it \
        -e CI="true" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        wagoodman/dive:latest $(APP_NAME)

hadolint:
	docker run --rm -i hadolint/hadolint < Dockerfile

dockle: docker-build
	docker run --rm -i \
        -v /var/run/docker.sock:/var/run/docker.sock \
        goodwithtech/dockle:latest -i CIS-DI-0006 -i CIS-DI-0005 $(APP_NAME)

docker-lint: hadolint dockle ## run docker image linters