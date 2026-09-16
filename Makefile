.PHONY: help install dev test lint clean setup run migrate seed

help:
	@echo "LogiSight Development Commands"
	@echo "=============================="
	@echo "make install          - Install dependencies"
	@echo "make dev              - Run development server"
	@echo "make test             - Run tests"
	@echo "make lint             - Run linting"
	@echo "make clean            - Clean up cache files"
	@echo "make setup            - Full setup (install + migrate + seed)"
	@echo "make migrate          - Run database migrations"
	@echo "make seed             - Generate synthetic data"
	@echo "make shell            - Flask shell"

install:
	pip install -r requirements.txt

dev:
	python run.py

test:
	pytest

lint:
	flake8 app tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

setup: install migrate seed
	@echo "Setup complete!"

migrate:
	flask db upgrade

seed:
	python scripts/generate_data.py

shell:
	flask shell
