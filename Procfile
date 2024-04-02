release: python manage.py makemigrations && python manage.py migrate

web: gunicorn travelers_tails_api.wsgi
