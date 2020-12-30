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

