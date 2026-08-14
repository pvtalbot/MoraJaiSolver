# Variables
PYTHON_FILES := src tests
UV := uv

.DEFAULT_GOAL := help

.PHONY: help install sync test test-cov lint format run check bench

help: ## Affiche ce message d'aide
	@echo "Commandes disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Installe l'environnement et toutes les dépendances
	$(UV) sync --all-extras --dev

sync: ## Synchronise l'environnement virtuel avec le lockfile
	$(UV) sync

test: ## Lance la suite de tests unitaires et E2E
	xvfb-run -a uv run pytest

test-cov: ## Lance les tests avec rapport de couverture
	xvfb-run -a uv run pytest --cov=src --cov-report=html

lint: ## Vérifie la qualité du code sans le modifier (CI)
	$(UV) run ruff check $(PYTHON_FILES)
	$(UV) run ruff format $(PYTHON_FILES) --check
	$(UV) run mypy $(PYTHON_FILES) --check-untyped-defs

format: ## Fix et formate automatiquement (dev)
	$(UV) run ruff format $(PYTHON_FILES)
	$(UV) run ruff check $(PYTHON_FILES) --fix

check: format lint test ## Exécute toute la CI en local (format + lint + tests)

run: ## Lance l'application
	$(UV) run morajai-solver

bench: ## Lance l'évaluation du solveur sur différentes grilles
	$(UV) run bench
