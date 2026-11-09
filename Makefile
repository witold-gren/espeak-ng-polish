# espeak-ng-polish - measure and improve the Polish rules of espeak-ng, the phonemizer behind Piper.
#
#   make help                       the steps in order (Polish or English, from $LANG; HELP_LANG=en|pl)
#   make <target> ESPEAK_SRC=<dir>  espeak-ng source tree with the changed rules (default below)
#
# Targets that need the Python environment create it first, so any target can be the first one.

# espeak-ng clone (later: your fork) where pl_rules / pl_list / ph_polish are edited
ESPEAK_SRC ?= ../espeak-ng
# espeak-ng binary used only as a compiler of the data files (macOS: brew install espeak-ng)
ESPEAK ?= espeak-ng
# `make branch`: ESPEAK_SRC is compared with its merge base with this ref (e.g. upstream/master, origin/master)
BASE_REF ?= upstream/master
# words or phrases for `make say`
TEXT ?= w domu grozić dzwon dźwięk Bydgoszcz
PYTHON ?= python3.12

VENV := .venv
CLI := $(VENV)/bin/espeak-pl
CANDIDATE := build/candidate/espeak-ng-data
HELP_LANG ?= $(if $(filter pl%,$(LANG)),pl,en)

.DEFAULT_GOAL := help
.PHONY: help setup doctor fetch baseline compile candidate compare report say patch-report upstream-test \
        branch test test-all docs clean

##@ Start | Start

help: ## This list | Ta lista
	@awk -v lang=$(HELP_LANG) 'BEGIN { FS = ":.*## " } \
	  /^##@ / { split(substr($$0, 5), t, " \\| "); printf "\n\033[1m%s\033[0m\n", (lang == "pl" && t[2] != "") ? t[2] : t[1]; next } \
	  /^[a-zA-Z0-9_-]+:.*## / { split($$2, d, " \\| "); printf "  \033[36m%-14s\033[0m %s\n", $$1, (lang == "pl" && d[2] != "") ? d[2] : d[1] }' \
	  $(MAKEFILE_LIST)
	@echo
	@if [ "$(HELP_LANG)" = "pl" ]; then \
	  echo "Źródła espeak-ng: ESPEAK_SRC=$(ESPEAK_SRC)   (zmień: make <cel> ESPEAK_SRC=/inna/ścieżka)"; \
	  echo "Środowisko: $(VENV) $$(test -x $(CLI) && echo '- gotowe' || echo '- powstanie przy pierwszym poleceniu')"; \
	else \
	  echo "espeak-ng sources: ESPEAK_SRC=$(ESPEAK_SRC)   (change: make <target> ESPEAK_SRC=/other/path)"; \
	  echo "Environment: $(VENV) $$(test -x $(CLI) && echo '- ready' || echo '- created by the first command')"; \
	fi

##@ 1. Setup | 1. Instalacja

$(CLI): pyproject.toml
	@echo "==> Python environment in $(VENV) ($(PYTHON))"
	@command -v $(PYTHON) >/dev/null || { echo "$(PYTHON) not found - macOS: brew install python@3.12"; exit 1; }
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/pip install -q --upgrade pip
	@$(VENV)/bin/pip install -q -e '.[test]'
	@touch $@
	@echo "==> ready: espeak-pl $$($(CLI) --version)"

setup: $(CLI) ## Create the environment with piper-tts (its espeak-ng) | Utwórz środowisko z piper-tts (i jego espeak-ng)

doctor: setup ## Check the tools: espeak-ng compiler, sources, word list | Sprawdź narzędzia: kompilator espeak-ng, źródła, słownik
	@command -v $(ESPEAK) >/dev/null && echo "ok   $$($(ESPEAK) --version | head -1)" || echo "MISSING $(ESPEAK) - macOS: brew install espeak-ng"
	@test -f $(ESPEAK_SRC)/dictsource/pl_rules && echo "ok   $(ESPEAK_SRC) ($$(git -C "$(ESPEAK_SRC)" rev-parse --abbrev-ref HEAD))" || echo "MISSING $(ESPEAK_SRC) - git clone https://github.com/espeak-ng/espeak-ng.git $(ESPEAK_SRC)"
	@test -f data/wikipron/pol_latn_broad.tsv && echo "ok   data/wikipron/pol_latn_broad.tsv" || echo "MISSING word list - make fetch"
	@$(VENV)/bin/python -c "import piper, importlib.metadata as m; print('ok   piper-tts', m.version('piper-tts'))"

fetch: setup ## Download the WikiPron Polish word list (Wiktionary, CC BY-SA) | Pobierz polski słownik WikiPron (Wikisłownik, CC BY-SA)
	$(CLI) fetch

##@ 2. Measure | 2. Pomiar

baseline: setup ## Measure espeak-ng as shipped in Piper | Zmierz espeak-ng w wersji z Pipera
	@test -f data/wikipron/pol_latn_broad.tsv || $(CLI) fetch
	$(CLI) evaluate wikipron --output reports/baseline-wikipron.json
	$(CLI) evaluate hard --output reports/baseline-hard.json
	$(CLI) report reports/baseline-wikipron.json --title "Baseline: WikiPron" --output reports/baseline-wikipron.md
	$(CLI) report reports/baseline-hard.json --title "Baseline: hard cases" --failures 200 --output reports/baseline-hard.md

compile: setup ## Build espeak-ng-data from ESPEAK_SRC (rules + phonemes) | Zbuduj espeak-ng-data z ESPEAK_SRC (reguły + fonemy)
	$(CLI) compile --source $(ESPEAK_SRC) --espeak $(ESPEAK) --phonemes

candidate: compile ## Measure the changed rules | Zmierz zmienione reguły
	$(CLI) evaluate wikipron --data-dir $(CANDIDATE) --output reports/candidate-wikipron.json
	$(CLI) evaluate hard --data-dir $(CANDIDATE) --output reports/candidate-hard.json
	$(CLI) report reports/candidate-wikipron.json --title "Candidate: WikiPron" --output reports/candidate-wikipron.md
	$(CLI) report reports/candidate-hard.json --title "Candidate: hard cases" --failures 200 --output reports/candidate-hard.md

compare: ## Fixed and broken words, baseline vs candidate (fails on any regression) | Naprawione i zepsute słowa, baza vs kandydat (błąd przy regresji)
	$(CLI) compare reports/baseline-wikipron.json reports/candidate-wikipron.json --output reports/compare-wikipron.md --strict
	$(CLI) compare reports/baseline-hard.json reports/candidate-hard.json --output reports/compare-hard.md --strict

report: baseline candidate compare ## Everything above in one go | Wszystko powyżej za jednym razem

say: setup ## Show IPA before/after: make say TEXT="w domu" | Pokaż IPA przed/po: make say TEXT="w domu"
	@echo "--- Piper (baseline)"; $(CLI) say $(TEXT)
	@test -d $(CANDIDATE) && { echo "--- candidate"; $(CLI) say --data-dir $(CANDIDATE) $(TEXT); } || echo "(no candidate yet - make compile)"

##@ 3. Upstream | 3. Wkład do espeak-ng

patch-report: setup ## Measure each patch in patches/ alone (for PR descriptions) | Zmierz każdą łatkę z patches/ osobno (do opisów PR)
	$(CLI) patch-report --source $(ESPEAK_SRC) --output reports/patches.md
	$(VENV)/bin/python tools/generate_patch_readme.py

branch: setup ## Measure a branch: ESPEAK_SRC vs its merge base with BASE_REF | Zmierz gałąź: ESPEAK_SRC względem bazy z BASE_REF
	@test -f data/wikipron/pol_latn_broad.tsv || $(CLI) fetch
	@base=$$(git -C "$(ESPEAK_SRC)" merge-base HEAD $(BASE_REF)) || { echo "no merge base with $(BASE_REF) - add the remote: git -C "$(ESPEAK_SRC)" remote add upstream https://github.com/espeak-ng/espeak-ng.git && git -C "$(ESPEAK_SRC)" fetch upstream"; exit 1; }; \
	  echo "==> base $$(git -C "$(ESPEAK_SRC)" log -1 --format='%h %cs %s' $$base)"; \
	  echo "==> branch $(ESPEAK_SRC) (HEAD $$(git -C "$(ESPEAK_SRC)" log -1 --format='%h %s'), uncommitted changes included)"; \
	  git -C "$(ESPEAK_SRC)" worktree remove --force "$$PWD/build/base-src" 2>/dev/null; rm -rf build/base-src; \
	  git -C "$(ESPEAK_SRC)" worktree add --quiet --detach "$$PWD/build/base-src" $$base
	$(CLI) compile --source build/base-src --output build/base --espeak $(ESPEAK) --phonemes
	$(CLI) compile --source "$(ESPEAK_SRC)" --output build/branch --espeak $(ESPEAK) --phonemes
	@git -C "$(ESPEAK_SRC)" worktree remove --force "$$PWD/build/base-src"
	@for s in wikipron hard; do \
	  echo "==> $$s: base"; $(CLI) evaluate $$s --data-dir build/base/espeak-ng-data --output reports/base-$$s.json || exit 1; \
	  echo "==> $$s: branch"; $(CLI) evaluate $$s --data-dir build/branch/espeak-ng-data --output reports/branch-$$s.json || exit 1; \
	  $(CLI) compare reports/base-$$s.json reports/branch-$$s.json --output reports/branch-compare-$$s.md || exit 1; \
	done
	@echo "==> lists of fixed and broken words: reports/branch-compare-wikipron.md, reports/branch-compare-hard.md"

upstream-test: compile ## Run the Polish lines of espeak-ng tests on the candidate | Uruchom polskie testy espeak-ng na kandydacie
	$(CLI) upstream-test --source $(ESPEAK_SRC) --espeak $(ESPEAK)

##@ 4. Development | 4. Rozwój

test: setup ## Tests of the tool | Testy narzędzia
	$(VENV)/bin/python -m pytest -q

test-all: test upstream-test ## Tests of the tool and Polish espeak-ng tests | Testy narzędzia i polskie testy espeak-ng

docs: ## Open the guide | Otwórz przewodnik
	@open docs/$(HELP_LANG).md 2>/dev/null || xdg-open docs/$(HELP_LANG).md

clean: ## Remove caches and builds (keeps environment, word list, reports) | Usuń pliki tymczasowe i buildy (środowisko, słownik i raporty zostają)
	find . -name __pycache__ -type d -prune -not -path "./.venv*" -exec rm -rf {} +
	rm -rf .pytest_cache build *.egg-info src/*.egg-info
