DOCKER ?= docker
DOCKER_COMPOSE ?= $(DOCKER) compose

BOOTSTRAP_SERVER ?= kafka1:29092

TOPIC ?= topic1
GROUP ?= group1

PARTITIONS ?= 3
REPLICATION ?= 1

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f || true

reboot: down up

topic:
	$(DOCKER_COMPOSE) exec kafka1 kafka-topics \
		--create \
		--topic $(TOPIC) \
		--partitions $(PARTITIONS) \
		--replication-factor $(REPLICATION) \
		--bootstrap-server $(BOOTSTRAP_SERVER)

producer:
	$(DOCKER_COMPOSE) exec kafka1 kafka-console-producer \
		--topic $(TOPIC) \
		--bootstrap-server $(BOOTSTRAP_SERVER)

consumer:
	$(DOCKER_COMPOSE) exec kafka1 kafka-console-consumer \
		--topic $(TOPIC) \
		--group $(GROUP) \
		--from-beginning \
		--bootstrap-server $(BOOTSTRAP_SERVER)
