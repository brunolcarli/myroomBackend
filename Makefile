install:
	pip install -r requirements.txt

shell:
	python3 manage.py shell

run:
	python3 manage.py runserver 0.0.0.0:6005
