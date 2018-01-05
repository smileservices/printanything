# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from customer.models import Customer
from django.http.response import JsonResponse
from contact.models import Contact
from django.shortcuts import render

# Create your views here.

def check_email(request):
    '''
    Returns False if customer does not exist or primary contact info
    :param email:
    :param request:
    :return:
    '''
    try:
        customer = Customer.objects.get(email=request.POST['email'])
        contact = customer.contact_set.filter(primary=True).first()
        if not contact:
            res = False
        else:
            res = {

            }
    except Customer.DoesNotExist:
        res = False
    return JsonResponse(res, safe=False)
