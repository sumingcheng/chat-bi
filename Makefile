docker_image_name ?= chat-bi
docker_image_tag ?= v1.0.0

dockerfile_path = deploy/Dockerfile
registry_prefix ?= ''

build:
	docker build -f $(dockerfile_path) -t $(docker_image_name):$(docker_image_tag) .

build-ufw:
	docker build --build-arg USE_CHINA_MIRROR=true -f $(dockerfile_path) -t $(docker_image_name):$(docker_image_tag) .

build-nocache:
	docker build --no-cache -f $(dockerfile_path) -t $(docker_image_name):$(docker_image_tag) .

run:
	cd deploy && docker-compose up -d

run-dev:
	cd deploy && docker-compose -f docker-compose-dev.yaml up -d

# 重头再来
reset:
	-@git pull
	-@cd deploy && docker-compose -f docker-compose-dev.yaml down
	-@docker rmi ${docker_image_name}:${docker_image_tag} || true
	-@$(MAKE) build
	-@cd deploy && docker-compose -f docker-compose-dev.yaml up -d

ddl:
	bash bin/get_db_ddl.sh

.PHONY: build build-nocache build-ufw run run-dev reset ddl