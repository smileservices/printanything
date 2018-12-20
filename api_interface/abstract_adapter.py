class Adapter:

    '''
        Abstract class for adapters
    '''

    def __init__(self, endpoint, user, key):
        self.endpoint = endpoint
        self.user = user
        self.key = key

    def place_order(self, order):
        raise NotImplementedError('Adapter\'s place_order method is not implemented!')
        pass

    def get_orders(self):
        raise NotImplementedError('Adapter\'s get_order method is not implemented!')
        pass

    def send_request(self):
        raise NotImplementedError('Adapter\'s send_request method is not implemented!')
        pass
