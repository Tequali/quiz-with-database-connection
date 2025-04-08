install:
	pip install -r requirements.txt

test:
	pytest test.py

run:
	python3 main.py