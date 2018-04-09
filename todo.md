# TODO:
- Finish the order phase
    - Order processing (place to vendor/status/shipment)
    - Implement cart/order reservation limited time
- Implement UI
    - redirect to paypal
    - payment success/cancel
- Add option to act as if no stock is needed (something like unlimited stock)
- clean up old carts (chron job)

## USERS
- admin users
- regular users

## ADMIN
- notification for new orders
- orders:
    - change statuses & delete

- Extra fields - add them in js
- test forms errors handling

## ORDER
- email template for notifications
- ticketing system
- after payment confirm delete cart

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
