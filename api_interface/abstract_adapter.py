class Adapter:

    # abstract class for adapters

    def __init__(self, endpoint, user, key):
        self.endpoint = endpoint
        self.user = user
        self.key = key

    def place_order(self, order):
        pass

    def get_orders(self):
        pass
