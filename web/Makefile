VERSION=v1.0.0
IMAGE_NAME=chat-bi-frontend

PHONY: build up down
build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f deploy/Dockerfile .

up:
	@cd deploy && docker-compose up -d

down:
	@cd deploy && docker-compose down

