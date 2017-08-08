.PHONY : venv
venv :
	virtualenv --python=python3 venv

reqs:
	pip install -r requirements/requirements.txt

test:
	venv/bin/python tests.py
