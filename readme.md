# About

An ecommerce app built on top of Django for selling personalized merchandise

# Deplyment

- Install package depedencies
```
    pip install -r requirements
```
- Make db migrations
```
    python manage.py migrate
```
- Change settings.py - STATIC_ROOT to point to a newly created folder that will store all project's static files
```
    python manage.py collectstatic
```
# Fixtures:
 - Useful for populating the database
 - Find in each sub-app in the fixtures/seed.json file
 - Apply them:
 ```
    python manage.py loaddata seed.json
    python manage.py dumpdata > seed.json
```

# Clean Up DB:
Delete all migration files
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```

# Plugins used:
 - Templating: https://github.com/petersirka/jquery.templates

