PYTHON ?= .venv/bin/python
PIP    ?= .venv/bin/pip
PACKAGES := uri2img2nl dsl2img2nl cli2img2nl

.PHONY: venv install install-dev test clean

venv:
	@test -d .venv || python3 -m venv .venv

install: venv
	$(PIP) install -e ".[analyze]"

install-dev: venv
	$(PIP) install -e ".[dev,analyze]"
	@for pkg in $(PACKAGES); do $(PIP) install -e packages/$$pkg; done

test:
	$(PYTHON) -m pytest tests/ -q --tb=short

clean:
	rm -rf .pytest_cache **/__pycache__ dist build *.egg-info
