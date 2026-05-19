.PHONY: help install validate render render-watch test lint clean

help:
	@echo "wko — Wiki Operating System"
	@echo ""
	@echo "Commands:"
	@echo "  make install        Cài Python deps"
	@echo "  make validate       Validate company.config.yaml"
	@echo "  make render         Render skills/ + docs/ → dist/"
	@echo "  make render-watch   Re-render khi source thay đổi"
	@echo "  make test           Chạy pytest"
	@echo "  make lint           Ruff + Black + markdownlint"
	@echo "  make clean          Xóa dist/, __pycache__/"

install:
	pip install -r scripts/requirements.txt
	pip install -e ".[dev]"

validate:
	python3 scripts/validate_config.py --strict

render:
	python3 scripts/render.py

render-watch:
	python3 scripts/render.py --watch

test:
	pytest

lint:
	ruff check scripts/ tests/
	black --check scripts/ tests/
	@command -v markdownlint-cli2 >/dev/null 2>&1 && markdownlint-cli2 "**/*.md" || echo "markdownlint-cli2 not installed, skip"

clean:
	rm -rf dist/ __pycache__/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
