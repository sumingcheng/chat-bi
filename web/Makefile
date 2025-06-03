VERSION=v1.0.0
IMAGE_NAME=chat-bi-frontend


build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f deploy/Dockerfile .

run:
	@cd deploy && docker-compose up -d

down:
	@cd deploy && docker-compose down

