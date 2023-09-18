install:
	pip install -r requirements.txt

shell:
	python3 manage.py shell

run:
	python3 manage.py runserver 0.0.0.0:6005

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

pipe:
	make install
	make migrate
	make run
