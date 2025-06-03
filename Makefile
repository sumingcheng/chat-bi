BACKEND_IMAGE_NAME ?= chat-bi-api
BACKEND_IMAGE_TAG ?= v1.0.0

DOCKERFILE_PATH = ./deploy/Dockerfile

build:
	docker build --build-arg USE_CHINA_MIRROR=true -f $(DOCKERFILE_PATH) -t $(BACKEND_IMAGE_NAME):$(BACKEND_IMAGE_TAG) .

up:
	cd deploy && docker-compose -f docker-compose.yaml up -d

down:
	cd deploy && docker-compose -f docker-compose.yaml down


