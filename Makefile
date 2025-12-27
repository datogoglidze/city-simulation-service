amend:
	git commit --amend --no-edit -a

install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install --no-root

lock:
	poetry lock

update:
	poetry update

format:
	poetry run ruff format app
	poetry run ruff check  app --fix

lint:
	poetry check --strict
	poetry run ruff format app --check
	poetry run ruff check  app
	poetry run mypy app


test:
	poetry run pytest tests/unit tests/integration --cov

run:
	python -m app.runner --host localhost --port 8000
