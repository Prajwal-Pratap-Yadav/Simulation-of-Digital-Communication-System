PYTHON ?= python3
VENV = .venv
PY = $(VENV)/bin/python

.PHONY: setup lint typecheck test run reproduce docs build security clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --require-hashes -r requirements.lock
	$(PY) -m pip install --no-build-isolation --no-deps -e .

lint:
	$(PY) -m ruff check src tests scripts
	$(PY) -m black --check src tests scripts

typecheck:
	$(PY) -m mypy src/commsim

test:
	$(PY) -m pytest -q

run:
	$(PY) -m commsim.cli --config configs/smoke.json --output reports/local/smoke

reproduce:
	$(PY) -m commsim.cli --config configs/default.json --output reports

docs:
	$(PY) scripts/check_docs.py

build:
	$(PY) -m build --no-isolation

security:
	gitleaks detect --log-opts="--all" --redact
	$(PY) -m pip_audit -r requirements-runtime.txt --strict

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in [Path('build'), Path('dist'), Path('reports/local')]]"
