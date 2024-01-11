install:
	@poetry install

start:
	@poetry run uvicorn app.server:app --reload

test: ## Run tests locally. Usage: "make test [path]" Example: "make test path=tests/controllers/"
	@poetry run pytest $(path)
