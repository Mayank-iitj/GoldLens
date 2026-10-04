.PHONY: setup ingest build backtest holdout verdict alerts app test lint demo

setup:
	poetry install
	poetry run pre-commit install

ingest:
	poetry run python -m goldlens.cli ingest --start 2020-01-01 --end today

build:
	poetry run python -m goldlens.cli build

backtest:
	poetry run python -m goldlens.cli backtest

holdout:
	poetry run python -m goldlens.cli backtest --confirm-holdout

verdict:
	poetry run python -m goldlens.cli verdict

alerts:
	poetry run python -m goldlens.cli alerts

app:
	poetry run streamlit run app/streamlit_app.py

test:
	poetry run pytest tests/

lint:
	poetry run ruff check .
	poetry run mypy src/goldlens

demo:
	poetry run python -m goldlens.cli demo
