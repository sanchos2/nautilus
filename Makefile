check:
	poetry run flake8 webapp
	poetry run pytest --cov=./ tests/ --cov-report=xml
