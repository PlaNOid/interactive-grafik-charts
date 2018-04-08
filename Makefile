.PHONY: dev build up migrate shell dbshell redis-cli test

COMPOSE-DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE-TEST = docker-compose -f docker-compose.yml -f docker-compose.test.yml

dev:
	$(COMPOSE-DEV) up --build

build:
	$(COMPOSE-DEV) build

up:
	$(COMPOSE-DEV) up

stop:
	$(COMPOSE-DEV) down

migrate:
	$(COMPOSE-DEV) exec ig flask db migrate

shell:
	$(COMPOSE-DEV) exec ig flask debug

bash:
	$(COMPOSE-DEV) exec ig bash

dbshell:
	$(COMPOSE-DEV) exec ig flask dbshell

redis-cli:
	$(COMPOSE-DEV) exec ig_redis redis-cli

test:
	$(COMPOSE-TEST) up --build
