# happymeter :blush:

[![Build](https://github.com/mixklim/happymeter/actions/workflows/build.yml/badge.svg)](https://github.com/mixklim/happymeter/actions/workflows/build.yml)
[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)

##### Find out how happy you are

ML model based on [Somerville Happiness Survey Data Set](https://archive.ics.uci.edu/ml/datasets/Somerville+Happiness+Survey#).

##### To run locally (from root folder):

- create virtual environment: `python -m venv .venv`
- install dependencies: `poetry install --no-root`
- launch backend:
  `poetry run uvicorn src.app.main:app --port=8080 --reload`
- launch front-end:
  `poetry run streamlit run src/streamlit/ui.py --server.port 8501`
- pre-commit: `poetry run pre-commit run --all-files`
- unit tests: `poetry run pytest --cov=. --cov-report=html`
- coverage badge:
  - `coverage report`
  - `coverage xml -o ./reports/coverage/coverage.xml`
  - `coverage html`
  - `move /y .\htmlcov\index.html .\reports\coverage`
  - `genbadge coverage --output-file reports/coverage/coverage-badge.svg`
- docker backend:
  - `docker build -t backend-image -f Dockerfile.backend .`
  - `docker run --name backend-container -p 8080:8080 --rm backend-image`
- docker frontend:
  - `docker build -t frontend-image -f Dockerfile.frontend .`
  - `docker run --name frontend-container -p 8501:8501 --rm frontend-image`
- docker compose:
  - `docker compose build`
  - `docker compose up`
