# NeetCode practice monorepo — one entry point for three stacks.
#
#   make setup                 install everything (once)
#   make status                which problems you have solved
#   make test                  run all six suites — RED until you solve things, by design
#   make show SLUG=two-sum     peek at a worked answer
#
# Run `make` with no target for the full list.

SHELL := /bin/bash
.DEFAULT_GOAL := help

VENV    := .venv
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
PYTEST  := $(VENV)/bin/pytest

.PHONY: help
help: ## Show this list
	@echo "NeetCode monorepo"
	@echo
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "Solve a problem:"
	@echo "  1. docs/problems/0001-two-sum.md        read the brief"
	@echo "  2. edit the three stubs it names"
	@echo "  3. make test                            red -> green"
	@echo
	@echo "Author a new exercise:"
	@echo "  make new-problem ARGS=\"--id 242 --slug valid-anagram --title 'Valid Anagram' \\"
	@echo "      --difficulty easy --topic arrays-and-hashing \\"
	@echo "      --input 's:string,t:string' --returns bool --approaches sorting,hash-map\""

# ---------------------------------------------------------------------------- setup

.PHONY: setup
setup: setup-python setup-node setup-php ## Install all three toolchains
	@echo
	@echo "Ready. Try: make test"

.PHONY: setup-python
setup-python: ## Create .venv and install core + api (editable)
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet -e "packages/core-python[dev]"
	$(PIP) install --quiet -e "apps/api-python[dev]"

.PHONY: setup-node
setup-node: ## npm install (workspaces) and build the core library
	npm install
	npm run build --workspace @neetcode/core

.PHONY: setup-php
setup-php: ## composer install for the core package and the Laravel app, + Laravel's .env
	cd packages/core-php && composer install --no-interaction
	cd apps/api-php && composer install --no-interaction
	@# Laravel needs a .env with an APP_KEY before artisan will serve. `composer
	@# create-project` normally does this via post-create-project-cmd, which this repo does
	@# not ship — a clone is not a create-project, so it has to happen here.
	@test -f apps/api-php/.env || { \
		cp apps/api-php/.env.example apps/api-php/.env; \
		cd apps/api-php && php artisan key:generate --ansi; \
	}

# ---------------------------------------------------------------------------- test

.PHONY: test
test: test-python test-node test-php ## Run every suite (6 suites, 3 languages)
	@echo
	@echo "All suites passed."

# NOTE: on a fresh clone `make test` FAILS, and that is the point — every algorithm is an
# unsolved exercise. `make status` shows what is still a stub.

.PHONY: test-python
test-python: ## pytest: core library + FastAPI app
	@echo "--- python: core ---"
	cd packages/core-python && ../../$(PYTEST) -q -p no:warnings
	@echo "--- python: api ---"
	cd apps/api-python && ../../$(PYTEST) -q -p no:warnings

.PHONY: test-node
test-node: ## vitest (core library) + jest/supertest (NestJS app)
	@echo "--- node: core ---"
	npm run test --workspace @neetcode/core
	@echo "--- node: api ---"
	npm run test --workspace @neetcode/api-node

.PHONY: test-php
test-php: ## phpunit: core package + Laravel app
	@echo "--- php: core ---"
	cd packages/core-php && ./vendor/bin/phpunit
	@echo "--- php: api ---"
	cd apps/api-php && php artisan test

.PHONY: sync
sync: ## Pull new problems from the platform into your solutions repo, keeping your solutions
	@$(PY) tools/sync_upstream.py $(if $(UPSTREAM),--upstream $(UPSTREAM),)

.PHONY: test-solved
test-solved: ## Test every problem you have solved, and only those. What CI runs in a solutions repo
	@$(PY) tools/test_solved.py

.PHONY: try
try: ## THE LOOP: run one problem in all three languages. SLUG=two-sum [LANG=python]
	@test -n "$(SLUG)" || { echo "Usage: make try SLUG=two-sum [LANG=python|typescript|php]"; exit 1; }
	@$(PY) tools/try_problem.py $(SLUG) $(if $(LANG),--lang $(LANG),) || true

.PHONY: test-contracts
test-contracts: ## Validate every contract file against the JSON schema
	$(PY) tools/validate_contracts.py

# ---------------------------------------------------------------------------- run

.PHONY: run-python
run-python: ## FastAPI on :8000  (docs at /docs)
	cd apps/api-python && ../../$(VENV)/bin/uvicorn neetcode_api.main:app --reload --port 8000

.PHONY: run-node
run-node: ## NestJS on :3000  (docs at /docs)
	npm run start:dev --workspace @neetcode/api-node

.PHONY: run-php
run-php: ## Laravel on :8080
	cd apps/api-php && php artisan serve --port=8080

.PHONY: run-all
run-all: ## All three at once, on 8000 / 3000 / 8080
	@echo "FastAPI :8000   NestJS :3000   Laravel :8080   (ctrl-c stops all)"
	@trap 'kill 0' EXIT; \
	 ( cd apps/api-python && ../../$(VENV)/bin/uvicorn neetcode_api.main:app --port 8000 ) & \
	 ( npm run start --workspace @neetcode/api-node ) & \
	 ( cd apps/api-php && php artisan serve --port=8080 ) & \
	 wait

# ---------------------------------------------------------------------------- quality

.PHONY: lint
lint: ## ruff + tsc + pint
	$(VENV)/bin/ruff check packages/core-python apps/api-python
	npx tsc --noEmit -p packages/core-ts/tsconfig.json
	npx tsc --noEmit -p apps/api-node/tsconfig.json
	cd apps/api-php && ./vendor/bin/pint --test

.PHONY: format
format: ## Autoformat everything it can
	$(VENV)/bin/ruff check --fix packages/core-python apps/api-python
	$(VENV)/bin/ruff format packages/core-python apps/api-python
	cd apps/api-php && ./vendor/bin/pint

.PHONY: typecheck
typecheck: ## mypy + tsc
	cd packages/core-python && ../../$(VENV)/bin/mypy
	npx tsc --noEmit -p packages/core-ts/tsconfig.json
	npx tsc --noEmit -p apps/api-node/tsconfig.json

# ---------------------------------------------------------------------------- solutions

.PHONY: status
status: ## Which problems are solved, per language
	@$(PY) tools/solutions.py status

.PHONY: show
show: ## Print a worked answer without touching any file. SLUG=two-sum [LANG=python]
	@test -n "$(SLUG)" || { echo "Usage: make show SLUG=two-sum [LANG=python|typescript|php]"; exit 1; }
	@$(PY) tools/solutions.py show --slug $(SLUG) $(if $(LANG),--lang $(LANG),)

.PHONY: solution
solution: ## Copy a worked answer over your stub. SLUG=two-sum [LANG=..] — `make restore` undoes it
	@test -n "$(SLUG)" || { echo "Usage: make solution SLUG=two-sum [LANG=python|typescript|php]"; exit 1; }
	@$(PY) tools/solutions.py apply --slug $(SLUG) $(if $(LANG),--lang $(LANG),)

.PHONY: restore
restore: ## Undo `make solution` / `make verify-solutions` — put your own files back
	@$(PY) tools/solutions.py restore

.PHONY: verify-solutions
verify-solutions: ## Apply every reference answer, run the full suite, then restore your files
	@echo "Applying reference solutions (your files are backed up)..."
	@$(PY) tools/solutions.py apply --force >/dev/null
	@npm run build --workspace @neetcode/core >/dev/null
	@$(MAKE) test; status=$$?; \
	 echo "Restoring your files..."; \
	 $(PY) tools/solutions.py restore >/dev/null; \
	 npm run build --workspace @neetcode/core >/dev/null; \
	 exit $$status

.PHONY: stubs
stubs: ## Regenerate stub hints from the contracts. Never touches solutions/ or solved files. [SLUG=x]
	@$(PY) tools/solutions.py restub $(if $(SLUG),--slug $(SLUG),)

.PHONY: extract
extract: ## Move YOUR implementation into solutions/ and leave a stub. SLUG=x, or omit for all
	@$(PY) tools/solutions.py extract $(if $(SLUG),--slug $(SLUG),)

# ---------------------------------------------------------------------------- authoring

.PHONY: new-problem
new-problem: ## Scaffold a problem across all three stacks (see ARGS below)
	@test -n "$(ARGS)" || { echo "Usage: make new-problem ARGS=\"--id 242 --slug ... \""; exit 1; }
	$(PY) tools/new_problem.py $(ARGS)

.PHONY: statements
statements: ## Regenerate docs/problems/*.md from the contracts
	$(PY) tools/render_statements.py

.PHONY: progress
progress: ## Print the NeetCode 150 progress table
	$(PY) tools/progress.py

# ---------------------------------------------------------------------------- misc

.PHONY: clean
clean: ## Remove build output and caches (keeps installed deps)
	rm -rf packages/core-ts/dist apps/api-node/dist
	find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	find . -name .pytest_cache -type d -prune -exec rm -rf {} + 2>/dev/null || true
	rm -f apps/api-php/.phpunit.result.cache packages/core-php/.phpunit.result.cache

.PHONY: clean-all
clean-all: clean ## Also remove installed dependencies
	rm -rf $(VENV) node_modules packages/core-php/vendor apps/api-php/vendor
