install:
	@poetry install
	@poetry run pre-commit install

db-up: ## Start database
	@docker-compose up -d

db-upgrade: ## Apply migrations
	@poetry run alembic upgrade head

db-downgrade: ## Downgrade migrations
	@poetry run alembic downgrade -1

db-seed: ## Seed database with test data
	@poetry run python scripts/db_seed.py

start:
	@poetry run uvicorn app.server:app --reload

db-migrate: ## Create migration with alembic. Usage: "make db-migrate message='migration message'"
	@poetry run alembic revision --autogenerate -m "$(message)"

start-port: ## Start server with specific port. Only needed on production. Usage: "make start-port PORT=8000"
	@poetry run alembic upgrade head 
	@poetry run uvicorn app.server:app --host 0.0.0.0 --port ${PORT}

test: ## Run tests locally. Usage: "make test [path]" Example: "make test path=tests/controllers/"
	@poetry run pytest $(path)
