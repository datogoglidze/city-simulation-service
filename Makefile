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
	poetry run ruff format app tests
	poetry run ruff check  app tests --fix

lint:
	poetry check --strict
	poetry run ruff format app tests --check
	poetry run ruff check app tests
	poetry run mypy app tests

test:
	poetry run pytest tests --cov

run:
	python -m app.runner --host localhost --port 8000

build:
	pip install poetry-plugin-export
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	docker build -t city-simulation-service:latest --build-arg RELEASE=$$(git rev-parse --short HEAD) .
	rm requirements.txt
