CICI_VENV_DIR=.dev-venv
CICI_TOX_EXTRA_ARGS ?=

.PHONY: help
help:
	@echo "python packaging help:"
	@echo ""
	@echo "make check-tox:"
	@echo "    Run tests against multiple python versions."
	@echo "    These tests use the newest dependencies."
	@echo "    Requires: Python 3.11 - 3.13, and tox."
	@echo "    Hint (Fedora): 'sudo dnf install python3-tox python3.13'"
	@echo "    The variable CICI_TOX_EXTRA_ARGS can be use to pass extra"
	@echo "    arguments to tox".
	@echo ""
	@echo "make check-dev:"
	@echo "    Run tests in a venv against your default python3 version."
	@echo "    These tests use the newest dependencies."
	@echo "    Requires: Python 3.x"
	@echo ""
	@echo "make check:"
	@echo "    Run tests in your *current environment*."
	@echo "    Performs no environment setup of any kind."
	@echo ""
	@echo "make develop:"
	@echo "    Install deps needed for 'make check',"
	@echo "    and install the cici package in editable mode."
	@echo "    (Can be used in or outside of a venv.)"
	@echo ""
	@echo "make dev-venv"
	@echo "    Creates a simple venv for check-dev. ($(CICI_VENV_DIR))"
	@echo ""
	@echo "make clean:"
	@echo "    Remove package build output."
	@echo ""
	@echo "make distclean:"
	@echo "    remove venv files, cici package forwarder,"
	@echo "    built distribution files, and everything from 'make clean'."
	@echo ""
	@echo -e "Have a nice day ^_^;\n"

PIP_INSTALL = pip install --disable-pip-version-check

.PHONY: dev-venv
dev-venv: $(CICI_VENV_DIR) $(CICI_VENV_DIR)/bin/activate
$(CICI_VENV_DIR) $(CICI_VENV_DIR)/bin/activate: setup.cfg
	@echo "VENV $(CICI_VENV_DIR)"
	@python3 -m venv $(CICI_VENV_DIR)
	@(								\
		echo "ACTIVATE $(CICI_VENV_DIR)";			\
		. $(CICI_VENV_DIR)/bin/activate;			\
		echo "INSTALL cici[devel] $(CICI_VENV_DIR)";		\
		make develop 1>/dev/null;				\
	)
	@touch $(CICI_VENV_DIR)

.PHONY: check-dev
check-dev: dev-venv
	@(							\
		echo "ACTIVATE $(CICI_VENV_DIR)";		\
		. $(CICI_VENV_DIR)/bin/activate;		\
		make check;					\
	)

.PHONY: develop
develop:
	$(PIP_INSTALL) -e .[devel] --config-settings=editable_mode=compat

.PHONY: check
check:
	@avocado --config avocado.cfg run tests/

.PHONY: check-tox
check-tox:
	@tox $(CICI_TOX_EXTRA_ARGS)

.PHONY: check-coverage
check-coverage:
	@coverage run -m avocado --config avocado.cfg run tests/*.py
	@coverage combine
	@coverage html
	@coverage xml
	@coverage report

.PHONY: clean
clean:
	rm -rf build/

.PHONY: distclean
distclean: clean
	rm -rf cici_toolkit.egg-info/ dist/
	rm -rf $(CICI_VENV_DIR) $(CICI_MINVENV_DIR) .tox/
	rm -f .coverage coverage.xml .coverage.*
	rm -rf htmlcov/ test-results/

.PHONY: tag
tag:
	python3 scripts/package.py tag

dist: setup.cfg MANIFEST.in README.rst scripts/package.py
	python3 scripts/package.py build

.PHONY: test-publish
test-publish:
	python3 scripts/package.py publish --test

.PHONY: publish
publish:
	python3 scripts/package.py publish
