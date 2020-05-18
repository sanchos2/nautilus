check:
    mdl README.md
	poetry run flake8 webapp
	poetry run pytest --cov=./ tests/ --cov-report=xml
	opensource_watchman sanchos2 --repo_name=nautilus
