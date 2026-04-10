all: build reload psql start stop

build:
	docker build -t callmentor-nginx ./nginx
	docker build -t callmentor-frontend ./callmentor-frontend
	docker build -t callmentor-gateway ./gateway/api
	docker build -t callmentor-ml-service ./ml-service
	docker build -t callmentor-ml-llm ./ml-llm
	docker build -t callmentor-ml-asr ./ml-asr
	docker build -t callmentor-bot ./bot

reload:
	docker compose up --no-recreate -d gateway-db gateway-redis ml-redis rabbitmq
	docker compose up --force-recreate -d nginx frontend gateway ml-service ml-llm-worker ml-asr-worker telegram-bot

psql:
	docker compose exec -it gateway-db psql -U backend -d gateway-db

start:
	docker compose up -d --build

stop:
	docker compose down
