.PHONY: install test lint format data research backtest figures reproduce

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m black src scripts tests
	python -m ruff check --fix src scripts tests

data:
	python scripts/build_dataset.py

research:
	python scripts/run_factor_research.py

backtest:
	python scripts/run_backtest.py

figures:
	python scripts/generate_report_artifacts.py

reproduce:
	python scripts/run_full_pipeline.py
