install:
	@poetry install
	@poetry run pre-commit install

start:
	@poetry run uvicorn app.server:app --reload

start-port:
	@poetry run alembic upgrade head 
	@poetry run uvicorn app.server:app --host 0.0.0.0 --port ${PORT}

test: ## Run tests locally. Usage: "make test [path]" Example: "make test path=tests/controllers/"
	@poetry run pytest $(path)

db-seed: ## Seed database with test data
	@poetry run python scripts/db_seed.py

db-up: ## Start database
	@docker-compose up -d

db-migrate: ## Create migration with alembic. Usage: "make db-migrate message='migration message'"
	@poetry run alembic revision --autogenerate -m "$(message)"

db-upgrade: ## Apply migrations
	@poetry run alembic upgrade head
