#!make
.EXPORT_ALL_VARIABLES:
-include .env

up:
	docker-compose up --build

up_dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
