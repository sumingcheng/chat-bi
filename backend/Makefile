BACKEND_IMAGE_NAME ?= chat-bi-api
BACKEND_IMAGE_TAG ?= v3.0.0

DOCKERFILE_PATH = ./Dockerfile

build:
	docker build --build-arg USE_CHINA_MIRROR=true -f $(DOCKERFILE_PATH) -t $(BACKEND_IMAGE_NAME):$(BACKEND_IMAGE_TAG) .

run:
	cd deploy && docker-compose -f docker-compose.yaml up -d

down:
	cd deploy && docker-compose -f docker-compose.yaml down

ddl:
	bash backend/bin/ddl_generate.sh

