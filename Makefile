install:
	poetry install

start:
	poetry run uvicorn app.server:app --reload
