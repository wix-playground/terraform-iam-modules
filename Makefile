.SILENT: format python_virtualenv_setup python_virtualenv_cleanup

PYTHON_BIN=python3
PIP_BIN=pip3

format:
	/usr/bin/env terraform fmt -list=true -recursive ./

python_virtualenv_setup:
	${PIP_BIN} install --upgrade virtualenv
	${PYTHON_BIN} -m virtualenv -p ${PYTHON_BIN} virtualenv; \
	source virtualenv/bin/activate; \
	pip install -r import_scripts/requirements.txt; \
	echo "Python virtualenv has been installed successfully."; \
	echo "To use it, type 'source virtualenv/bin/activate' in your console."

python_virtualenv_cleanup:
	rm -rf virtualenv; \
	find . -name '*.pyc' -delete; \
	echo "Python virtualenv has been removed successfully."