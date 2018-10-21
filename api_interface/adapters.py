###
#
# Contains functions for creating requests for the specified API service
#
###
from api_interface.abstract_adapter import Adapter


def get_all_adapters():
    adapters = [
        ('Pwinty', 'Pwinty'),
        ('Printful', 'Printful')
    ]
    return adapters


class Pwinty(Adapter):

    def place_order(self, order):
        pass

    def get_orders(self):
        pass


class Printful(Adapter):

    def place_order(self, order):
        pass

    def get_orders(self):
        pass
