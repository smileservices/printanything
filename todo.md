# TODO:
- Finish the order phase
    - Order processing (place to vendor/status/shipment)
    - Implement cart/order reservation limited time
    - after clicking "place order"
        - clear up cart
        - send email with order
    - admin order management
- Implement UI
    - redirect to paypal
    - payment success/cancel
- Add option to act as if no stock is needed (something like unlimited stock)

## USERS
- admin users
- regular users

## ADMIN
- notification for new orders
- orders:
    - list
    - view
    - edit

- Art create - add photo in js
- supports admin create stock options
- vendor admin - crud colors/sizes
- test forms errors handling

## ORDER
- email notifications
- ticketing system

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
