web: gunicorn btwitter.wsgi --log-file -
web: pip install -r requirements.txt
web: python manage.py makemigrations
web: python manage.py migrate
web: python manage.py runserver