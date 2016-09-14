PROJECT_DIR=$(shell pwd)
VENV_DIR?=$(PROJECT_DIR)/.env
PIP?=$(VENV_DIR)/bin/pip3
PYTHON?=$(VENV_DIR)/bin/python
ALEMBIC?=$(VENV_DIR)/bin/alembic


.PHONY: all clean test requirements install virtualenv

all: clean virtualenv install_pip install create_db create_tables populate

virtualenv:
	virtualenv -p python3.5 $(VENV_DIR) --no-site-packages

install:
	$(PYTHON) setup.py develop

install_pip:
	$(PIP) install -U pip wheel setuptools

create_db:
	sudo -u postgres psql -f ./install/db/create_db.sql

create_tables:
	$(ALEMBIC) upgrade head

populate_books:
	$(PYTHON) $(PROJECT_DIR)/install/db/populate/books.py

populate: populate_books

clean_temp:
	find . -name '*.pyc' -delete
	rm -rf .coverage dist docs/_build htmlcov MANIFEST logs

clean_venv:
	rm -rf $(VENV_DIR)

run:
	$(VENV_DIR)/bin/pserve development.ini --reload

shell:
	$(VENV_DIR)/bin/pshell development.ini
