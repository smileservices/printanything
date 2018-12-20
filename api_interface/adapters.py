###
#
# Contains functions for creating requests for the specified API service
#
###
from api_interface.abstract_adapter import Adapter
from api_interface.printful.printful import PrintfulClient

def get_all_adapters():
    adapters = [
        ('Pwinty', 'Pwinty'),
        ('Printful', 'Printful')
    ]
    return adapters


class Pwinty(Adapter):

    def place_order(self, order):
        '''
        :param order: Order instance
        :return: API response

        1. Create order
        2. Add products to order
        3. Check if order is valid
        4. Submit the order
        '''
        pass

    def get_orders(self):
        pass


class Printful(Adapter):

    def __init__(self, endpoint, user, api_key):
        self.printful = PrintfulClient()


    def place_order(self, order):
        pass

    def get_orders(self):
        pass
