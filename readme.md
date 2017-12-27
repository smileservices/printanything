# TODO:
    - Finish the order phase
        - Order Placement
        - Payment
        - Order processing (place to vendor/status/shipment)
    - Implement UI

# Fixtures:
 - Useful for populating the database
 - Find in each sub-app in the fixtures/seed.json file
 - Apply them:
    python manage.py loaddata seed.json
    python manage.py dump seed.json


# Clean Up DB:
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete


