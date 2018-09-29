# TODO:
Overlay art on support
- set up printable area
- use html canvas to overlay art on said area

1 new image gallery used for art placement has print coordinates for each image. art is put on that area
    printing area position is relative to the center of image
3 separate support gallery appears bellow the main image and open in gallery mode
4 art images gallery
5 single art image for mockuping
6 when adding to basket a temp image is created of the art/support and referenced in the order. if the order is canceled/deleted, it will be deleted as well. will be sent to vendor if the order is placed
7 order details - refactor to use product_image
8 link to vendor size chart for every support

- stop using inline formset for images; use separate form


Admin
- fix uploading multiple imgs to supports
- each support must have at least one img set as primary

## FRONTEND UI
- Design UI (designer)
    - redirect to paypal
    - payment success/cancel - use big shop one

FUTURE RELEASES

### Order
- add option to act as if no stock is needed (something like unlimited stock)
- Implement cart/order reservation limited time
- clean up old carts (chron job)
- add "edited on" time column in view/detail
- ticketing system for customer/vendor/admin
- add elasticsearch
- update shipping info?
- email template for notifications


