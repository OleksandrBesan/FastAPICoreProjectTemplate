include .env
export $(shell sed 's/=.*//' .env)

local_build:
	docker build -t projectName .

run_docker_build:
	docker run -d --name projectName -p 8000:8000 projectName

run_poetry_project:
	poetry run uvicorn main:app --reload --app-dir src

coveragereport:
	poetry run coverage report -m

precommit:
	pre-commit run --all-files

linter:
	flake8 .

type_check:
	mypy .
