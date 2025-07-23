# Makefile for clausemate project development tasks
# NOTE: For cross-platform compatibility, consider using 'nox' instead
# See noxfile.py for modern Python task automation

.PHONY: help install test lint format type-check clean build docs

help: ## Show this help message
	@echo "Available commands:"
	@echo "NOTE: For better cross-platform support, consider using 'nox' (see noxfile.py)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e ".[dev]"

install-hooks: ## Install pre-commit hooks
	pre-commit install

test: ## Run all tests
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

test-fast: ## Run fast tests only
	pytest tests/ -v -m "not slow"

test-integration: ## Run integration tests
	python src/main.py
	python archive/phase1/clause_mates_complete.py
	python archive/phase_comparison/compare_phases.py

lint: ## Run all linting tools
	ruff check src/ tests/

format: ## Format code with ruff
	ruff format src/ tests/

format-check: ## Check code formatting
	ruff format --check src/ tests/

lint-fix: ## Run linting with auto-fix
	ruff check --fix src/ tests/

type-check: ## Run type checking
	mypy src/

quality: lint type-check format-check ## Run all quality checks

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	python -m build

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"
	@echo "Consider adding sphinx or mkdocs"

benchmark: ## Run performance benchmarks
	python -m pytest tests/ -m "benchmark" --benchmark-only

profile: ## Profile main execution
	python -m cProfile -o profile.stats src/main.py
	python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

memory-profile: ## Memory profiling
	python -m memory_profiler src/main.py

docker-build: ## Build Docker image
	docker build -t clausemate:latest .

docker-run: ## Run in Docker container
	docker run --rm -v $(PWD)/data:/app/data clausemate:latest

docker-test: ## Test in Docker container
	docker run --rm clausemate:latest python -m pytest tests/ -v

validate-setup: ## Validate complete setup
	@echo "Validating development setup..."
	python --version
	pip check
	pre-commit --version
	pytest --version
	mypy --version
	ruff --version
	@echo "Setup validation complete!"

# Development workflow targets
dev-setup: install install-hooks ## Set up development environment
	@echo "Development environment setup complete!"

ci-test: test lint lint-fix type-check format-check ## Run CI-equivalent tests locally

release-check: clean build test ci-test ## Pre-release validation
