# TODO:
    - Finish the order phase
        - Cart page
        - Order Placement
        - Payment
        - Order processing (place to vendor/status/shipment)
        - Implement cart/order reservation limited time
    - Implement UI

# Fixtures:
 - Useful for populating the database
 - Find in each sub-app in the fixtures/seed.json file
 - Apply them:
    python manage.py loaddata seed.json
    python manage.py dumpdata > seed.json


# Clean Up DB:
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete


# Plugins used:
 - Templating: https://github.com/petersirka/jquery.templates


