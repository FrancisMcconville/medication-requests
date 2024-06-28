
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
	docker compose up postgres --wait
	set -a && . .env.dev && \
	alembic upgrade head && \
	alembic revision --autogenerate
