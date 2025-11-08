export PYTHONPATH := $(PWD)

run_db:
	docker-compose up -d stonal-db