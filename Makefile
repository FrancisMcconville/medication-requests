
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
	&& pip install -r requirements.txt -r requirements_test.txt -r requirements_dev.txt

.PHONY: start-docker-infra
start-docker-infra:  ## Start any required infra using docker
	docker compose up --wait

.PHONY: start-docker-test-infra
start-docker-test-infra:  ## Start infra needed for testing using docker
	docker compose -f docker-compose-test.yml up --wait

.PHONY: run
run: .venv  ## Run the application locally
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	uvicorn src.main:app --reload

.PHONY: run-docker
run-docker:  ## Build and run the application in docker
	$(MAKE) start-docker-infra
	docker compose --profile api up

.PHONY: all
all:
	@echo todo

.PHONY: clean
clean:
	@echo todo

.PHONY: test
test: .venv ## Run Pytest
	$(MAKE) start-docker-test-infra
	. .venv/bin/activate && \
	set -a && . ./.env.test \
 	&& pytest tests

.PHONY: alembic-revision
alembic-revision:  ## Autogenerate a new alembic migration
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	alembic upgrade head && \
	alembic revision --autogenerate

.PHONY: alembic-migrate
alembic-migrate:  ## Apply alembic migrations up to head
	$(MAKE) start-docker-infra
	set -a && . .env.dev && \
	alembic upgrade head
