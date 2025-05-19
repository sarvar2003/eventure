run:
	docker-compose up --build

stop:
	docker-compose stop

shell:
	docker-compose run --rm web python manage.py shell

superuser:
	docker-compose run --rm web python manage.py createsuperuser

migrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

sync_migrate:
	docker-compose run --rm web python manage.py migrate --run-syncdb 

test:
	docker-compose run --rm web python manage.py test