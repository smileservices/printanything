from django.views.generic.edit import CreateView, UpdateView, DeleteView
from admin.mixins import IsAdminMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from vendor.models import Vendor, Shipping


class VendorShippingUpdate(IsAdminMixin, UpdateView):
    model = Shipping
    template_name = "admin/shipping/form.html"
    fields = ("name", "price", "description")

    def get_success_url(self):
        return reverse_lazy('update-vendor', kwargs={'pk': self.object.vendor.id})


class VendorShippingCreate(IsAdminMixin, CreateView):
    model = Shipping
    template_name = "admin/shipping/form.html"
    fields = ("name", "price", "description")

    def get_success_url(self):
        return reverse_lazy('update-vendor', kwargs={'pk': self.vendor.id})

    def dispatch(self, request, *args, **kwargs):
        self.vendor = get_object_or_404(Vendor, pk=kwargs['vendor'])
        return super(VendorShippingCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendor = self.vendor
        return super(VendorShippingCreate, self).form_valid(form)


class VendorShippingDelete(IsAdminMixin, DeleteView):
    model = Shipping

    def get_success_url(self):
        return reverse_lazy('update-vendor', kwargs={'pk': self.object.vendor.id})
