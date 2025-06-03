VERSION=v1.0.0
IMAGE_NAME=chat-bi

.PHONY: build run clean up down
build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f deploy/Dockerfile .

run:
	python main.py

clean:
	docker rmi $(IMAGE_NAME):$(VERSION)

up:
	@cd deploy && docker-compose up -d

down:
	@cd deploy && docker-compose down

re:
	make build && make down && make up
