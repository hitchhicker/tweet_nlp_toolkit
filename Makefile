install: ## [Local development] Upgrade pip, install requirements, install package.
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt
	python -m pip install -e .

install-dev: ## [Local development] Install test requirements
	python -m pip install -r requirements-test.txt

lint: ## [Local development] Run mypy, pylint and black
	python -m mypy tweet_nlp_toolkit
	python -m pylint tweet_nlp_toolkit
	python -m black --check -l 120 tweet_nlp_toolkit

black: ## [Local development] Auto-format python code using black
	python -m black -l 120 tweet_nlp_toolkit

test: ## [Local development] Run unit tests
	python -m pytest -x -v tests