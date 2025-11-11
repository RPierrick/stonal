export PYTHONPATH := $(PWD)

run_server:
	docker-compose up --build

run_db:
	docker-compose up -d --build stonal-db

run_api:
	docker-compose up -d --build stonal-api

test:
	pytest

precommit:
	pre-commit run --all-files

score:
	pylint app

migrate: 
	alembic upgrade head
