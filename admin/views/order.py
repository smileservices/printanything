from django.http import HttpResponseRedirect

import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from admin.mixins import IsAdminMixin
from django.urls import reverse_lazy
from order.models import Order, OrderStatus


class OrderView(IsAdminMixin, DetailView):
    model = Order
    template_name = "admin/order/view.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['orders_statuses'] = OrderStatus.objects.all()
        return context


def order_update(request, *args, **kwargs):
    section = request.POST['order-section']
    order = Order.objects.get(pk=kwargs.get('pk'))
    if section == "order-info":
        order.status_id = request.POST['order-status']
        order.info = request.POST['order-info']
        order.save()
    elif section == "order-shipping":
        shipping_detail = order.shippingdetails_set.get()
        shipping_detail.status = request.POST['shipping-status']
        shipping_detail.save()
    return HttpResponseRedirect(reverse_lazy("admin-orders"))


def order_to_vendor(request, order):
    order.vendor.place_order(order, 'https://' if request.is_secure() else 'http://' + request.get_host())
    order.info = 'Sent to vendor on {}'.format(datetime.date.today())
    order.save()


def order_process(request, *args, **kwargs):
    order = Order.objects.get(pk=kwargs.get('pk'))
    action = request.POST['action']
    if action == 'delete':
        order.order_group.delete_order(order)
    if action == 'close':
        order.mark_shipped()
    if action == 'to_vendor':
        order_to_vendor(request, order)
    return HttpResponseRedirect(reverse_lazy("admin-orders"))


class OrderStatusUpdate(IsAdminMixin, UpdateView):
    model = OrderStatus
    template_name = "admin/order/status-form.html"
    fields = ("id", "text")
    success_url = reverse_lazy("order-statuses")


class OrderStatusCreate(IsAdminMixin, CreateView):
    model = OrderStatus
    template_name = "admin/order/status-form.html"
    fields = ("id", "text")
    success_url = reverse_lazy("order-statuses")
