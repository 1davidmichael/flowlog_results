.PHONY : venv
venv :
	virtualenv --python=python3 venv

reqs:
	pip install -r requirements.txt
