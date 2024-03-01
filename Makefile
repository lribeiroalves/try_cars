install:
	pip install --upgrade pip
	pip install -r .\requirements.txt
	pip install -e .

test:
	cls
	pytest .\tests\ -v --cov=trycars
	coverage html
