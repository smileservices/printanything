from django.db import models
from api_interface import adapters


class ApiInterface(models.Model):
    '''
    Interface to various vendor api adapters
    '''
    name = models.CharField(max_length=128)
    endpoint = models.CharField(max_length=128)
    api_user = models.CharField(max_length=256)
    api_key = models.CharField(max_length=256)
    adapter = models.CharField(max_length=16, choices=adapters.get_all_adapters())

    def place(self, order):
        adapter_class_ = getattr(adapters, self.adapter)
        adapter_ = adapter_class_(self.endpoint, self.api_user, self.api_key)
        result = adapter_.place_order(order)
        return result

    def __str__(self):
        return self.name
