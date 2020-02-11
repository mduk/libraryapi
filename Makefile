deps:
	pipenv install

test:
	pipenv run pytest

dev:
	pipenv run ./main.py
