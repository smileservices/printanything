# About

An ecommerce app built on top of Django for selling personalized merchandise

# Deplyment

- Install package depedencies

    pip install -r requirements

- Make db migrations

    python manage.py migrate

- Change settings.py - STATIC_ROOT to point to a newly created folder that will store all project's static files

    python manage.py collectstatic
