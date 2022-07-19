.PHONY: all

SHELL=/bin/bash -e

.DEFAULT_GOAL := help

lint:
	poetry run python -m flake8 ./

format:
	poetry run autopep8 --aggressive --experimental -r -i ./ 
	poetry run python -m isort ./
	poetry run black --fast ./