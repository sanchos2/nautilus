check:
    mdl README.md
    poetry run flake8
    poetry run pytest --cov=./ tests/
