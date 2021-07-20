install:
	poetry install

gendiff:
	poetry run gendiff

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

package-uninstall:
	python3 -m pip uninstall hexlet-code

test:
	poetry run pytest
	
test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml
