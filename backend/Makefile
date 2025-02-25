docker_image_name ?= chat-bi-api
docker_image_tag ?= v1.0.1

dockerfile_path = ./Dockerfile

build:
	docker build --build-arg USE_CHINA_MIRROR=true -f $(dockerfile_path) -t $(docker_image_name):$(docker_image_tag) .

run:
	cd deploy && docker-compose -f docker-compose.yaml up -d

down:
	cd deploy && docker-compose -f docker-compose.yaml down

ddl:
	bash backend/bin/ddl_generate.sh

