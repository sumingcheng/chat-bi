FRONTEND_IMAGE_NAME ?= chat-bi-frontend
FRONTEND_IMAGE_TAG ?= v1.0.0

DOCKERFILE_PATH = ./Dockerfile

build:
	docker build -f $(DOCKERFILE_PATH) -t $(FRONTEND_IMAGE_NAME):$(FRONTEND_IMAGE_TAG) .

run:
	cd ../deploy && docker-compose -f docker-compose.yaml up -d

down:
	cd ../deploy && docker-compose -f docker-compose.yaml down