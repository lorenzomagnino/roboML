.PHONY: init install run test lint format pre-commit-install clean help

help:
	@echo "Available commands:"
	@echo "  make init                 - Initialize project, dependencies, and hooks"
	@echo "  make install              - Install dependencies with uv"
	@echo "  make run                  - Run main.py"
	@echo "  make test                 - Run tests"
	@echo "  make lint                 - Run ruff linter"
	@echo "  make format               - Run black formatter"
	@echo "  make pre-commit-install   - Install pre-commit hooks"
	@echo "  make clean                - Clean cache files"

init:
	$(MAKE) install
	.venv/bin/python scripts/init_project.py
	$(MAKE) pre-commit-install
	@echo "Virtual environment ready. Activate it with: source .venv/bin/activate"

install:
	uv venv
	uv pip install hydra-core wandb torch omegaconf ruff black pytest pre-commit rich

run:
	.venv/bin/python main.py

test:
	.venv/bin/pytest tests/

lint:
	.venv/bin/ruff check .

format:
	.venv/bin/black .

pre-commit-install:
	.venv/bin/pre-commit install

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf outputs/
	rm -rf .hydra/
