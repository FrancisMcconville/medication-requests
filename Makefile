
.PHONY: help
help:  ## List all goals in makefile with brief documentation.
	@echo "$(notdir $(CURDIR))"
	@echo
	@echo "Available commands:"
	@sed -nr 's/(.*?):[^#]*##(.*)/    \1|\2/p' $(MAKEFILE_LIST) | column -s\| -t

.venv setup:  ## Setup Python venv.
	python3 -m venv .venv \
	&& . .venv/bin/activate \
	&& pip install wheel \
	&& pip install -r requirements.txt

.PHONY: start-docker-infra
start-docker-infra:
	docker compose up --wait

.PHONY: run
run: .venv
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	uvicorn src.main:app --reload

.PHONY: all
all:
	@echo todo

.PHONY: clean
clean:
	@echo todo

.PHONY: test
test:
	@echo todo

.PHONY: alembic-revision
alembic-revision:
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	alembic upgrade head && \
	alembic revision --autogenerate

.PHONY: alembic-migrate
alembic-migrate:
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	alembic upgrade head
