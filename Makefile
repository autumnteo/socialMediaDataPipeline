pytest:
	python -m pytest --log-cli-level info -p no:warnings -v ./tests

format:
	python -m black -S --line-length 79 --preview ./
	isort ./

type:
	python -m mypy --no-implicit-reexport --ignore-missing-imports --no-namespace-packages ./

lint:
	flake8 ./socialMediaPipeline
	flake8 ./tests

ci: format type lint pytest

reddit-etl:
	python ./socialMediaPipeline/main.py --etl reddit --tx sd --log info

twitter-etl:
	python ./socialMediaPipeline/main.py --etl twitter --log info

db:
	sqlite3 ./data/socialMediaPipeline.db

reset-db:
	python ./socialMediaPipeline/db_manager.py --reset-db