from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from admin.mixins import IsAdminMixin
from admin.forms import UserForm, VendorForm, ArtistForm, ArtForm, SupportForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from vendor.models import Vendor, Shipping
from artist.models import Artist
from product.models import Art, Support, Stock, Colour, Size
from order.models import Order, OrderStatus


def dashboard(request):
    if request.user.is_staff:
        return render(request, 'admin/dashboard.html')
    else:
        return redirect(settings.LOGIN_URL)


class CreateUser(IsAdminMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'admin/user/user_form.html'

    success_url = reverse_lazy('create_user')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create New User'
        context['submit_text'] = 'Create'
        return context

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)


class UpdateUser(IsAdminMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'admin/user/user_form.html'

    success_url = reverse_lazy('admin-users')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update User'
        context['submit_text'] = 'Update'
        return context

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)


class CreateVendor(IsAdminMixin, CreateView):
    form_class = VendorForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Vendor'
        context['submit_text'] = 'Create'
        context['size_formset'] = VendorForm.SizeFormset() if "validated_size_form" not in kwargs else kwargs[
            "validated_size_form"]
        context['colour_formset'] = VendorForm.ColourFormset() if "validated_colour_form" not in kwargs else kwargs[
            "validated_colour_form"]
        return context

    def form_valid(self, vendor_form):
        if not vendor_form.is_valid():
            return self.render_to_response(form=vendor_form)
        success_url = super(CreateVendor, self).form_valid(vendor_form)
        size_formset = VendorForm.SizeFormset(self.request.POST, instance=self.object)
        colour_formset = VendorForm.ColourFormset(self.request.POST, instance=self.object)
        valid = size_formset.is_valid() and colour_formset.is_valid()
        if valid:
            size_formset.save()
            colour_formset.save()
        else:
            context_data = self.get_context_data(validated_size_form=size_formset, validated_colour_form=colour_formset)
            return self.render_to_response(context_data)
        return success_url

    def post(self, request, *args, **kwargs):
        vendor_form = VendorForm(request.POST, request.FILES)
        return self.form_valid(vendor_form)


class UpdateVendor(IsAdminMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Vendor'
        context['submit_text'] = 'Update'
        context['supports'] = self.object.support_set.all()
        context['size_formset'] = VendorForm.SizeFormset(
            instance=self.object) if "validated_size_form" not in kwargs else kwargs["validated_size_form"]
        context['colour_formset'] = VendorForm.ColourFormset(
            instance=self.object) if "validated_colour_form" not in kwargs else kwargs["validated_colour_form"]
        return context

    def form_valid(self, vendor_form, size_formset, colour_formset):
        success_url = super(UpdateVendor, self).form_valid(vendor_form)
        valid = size_formset.is_valid() and colour_formset.is_valid()
        if valid:
            size_formset.save()
            colour_formset.save()
        else:
            validated_forms_context = self.get_context_data(form=vendor_form, validated_size_form=size_formset,
                                                            validated_colour_form=colour_formset)
            return self.render_to_response(validated_forms_context)
        return success_url

    def post(self, request, *args, **kwargs):
        vendor = Vendor.objects.get(pk=kwargs.get('pk'))
        vendor_form = VendorForm(request.POST, instance=vendor)
        size_formset = VendorForm.SizeFormset(request.POST, instance=vendor)
        colour_formset = VendorForm.ColourFormset(request.POST, instance=vendor)
        return self.form_valid(vendor_form, size_formset, colour_formset)


class CreateSupport(IsAdminMixin, CreateView):
    model = Support
    form_class = SupportForm
    template_name = 'admin/support/form.html'
    success_url = reverse_lazy('admin-supports')

    def get_context_data(self, **kwargs):
        context = super(CreateSupport, self).get_context_data(**kwargs)
        context['stock_forms'] = SupportForm().StockFormSet() if "validated_stocks_form" not in kwargs else kwargs[
            "validated_stocks_form"]
        context['images_form'] = SupportForm.ProductImageFormSet(
            instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]

        # filter the colour and size options for current vendor
        curr_vend = Vendor.objects.get(id=self.kwargs['vendorid'])
        for form in context['stock_forms']:
            form.fields['colour'].queryset = Colour.objects.filter(vendor=curr_vend)
            form.fields['size'].queryset = Size.objects.filter(vendor=curr_vend)
        context['vendor_id'] = self.kwargs['vendorid']
        context['action'] = 'Create'
        return context

    def form_valid(self, support_form):
        success_redirect = super(CreateSupport, self).form_valid(support_form)
        stock_formset = support_form.StockFormSet(data=self.request.POST, instance=self.object)
        valid = stock_formset.is_valid()
        if valid:
            stock_formset.save()
        validated_forms_context = self.get_context_data(form=support_form, validated_stocks_form=stock_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        support_form = SupportForm(data=request.POST)
        return self.form_valid(support_form)


class UpdateSupport(IsAdminMixin, UpdateView):
    model = Support
    form_class = SupportForm
    template_name = 'admin/support/form.html'
    success_url = reverse_lazy('admin-supports')

    def get_context_data(self, **kwargs):
        context = super(UpdateSupport, self).get_context_data(**kwargs)
        context['stock_forms'] = SupportForm.StockFormSet(
            instance=self.object) if "validated_stocks_form" not in kwargs else kwargs["validated_stocks_form"]
        context['images_form'] = SupportForm.ProductImageFormSet(
            instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]
        # filter the colour and size options for current vendor
        curr_vend = context['object'].vendor
        for form in context['stock_forms']:
            form.fields['colour'].queryset = Colour.objects.filter(vendor=curr_vend)
            form.fields['size'].queryset = Size.objects.filter(vendor=curr_vend)
        for form in context['images_form']:
            form.fields['colour'].queryset = Colour.objects.filter(vendor=curr_vend)
        context['action'] = 'Update'
        context['vendor_id'] = curr_vend.id
        return context

    def form_valid(self, form):
        support = form.save()
        success_redirect = super(UpdateSupport, self).form_valid(form)
        stock_formset = form.StockFormSet(self.request.POST, instance=support)
        images_formset = form.ProductImageFormSet(self.request.POST, self.request.FILES, instance=support)
        valid = stock_formset.is_valid() and images_formset.is_valid()
        if valid:
            stock_formset.save()
            images_formset.save()
        validated_forms_context = self.get_context_data(form=form, validated_stocks_form=stock_formset,
                                                        validated_images_form=images_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        support = Support.objects.get(pk=kwargs.get('pk'))
        support_form = SupportForm(data=request.POST, instance=support)
        return self.form_valid(support_form)


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
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendor = self.vendor
        return super(CreateView, self).form_valid(form)


class VendorShippingDelete(IsAdminMixin, DeleteView):
    model = Shipping

    def get_success_url(self):
        return reverse_lazy('update-vendor', kwargs={'pk': self.object.vendor.id})


class CreateArtist(IsAdminMixin, CreateView):
    form_class = ArtistForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Artist'
        context['submit_text'] = 'Create'
        return context


class UpdateArtist(IsAdminMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-artists')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Artist'
        context['submit_text'] = 'Update'
        return context


class CreateArt(IsAdminMixin, CreateView):
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-art')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Art'
        context['submit_text'] = 'Create'
        context['images_form'] = ArtForm.ImagesFormSet(
            instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]
        return context

    def form_valid(self, form):
        art = form.save()
        success_redirect = super(CreateArt, self).form_valid(form)
        images_formset = form.ImagesFormSet(self.request.POST, self.request.FILES, instance=art)
        valid = images_formset.is_valid()
        if valid:
            images_formset.save()
        validated_forms_context = self.get_context_data(form=form, validated_images_form=images_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        art_form = ArtForm(data=request.POST)
        return self.form_valid(art_form)


class UpdateArt(IsAdminMixin, UpdateView):
    model = Art
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-art')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Art'
        context['submit_text'] = 'Update'
        context['images_form'] = ArtForm.ImagesFormSet(
            instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]
        return context

    def form_valid(self, form, images_formset):
        success_redirect = super(UpdateArt, self).form_valid(form)
        valid = images_formset.is_valid()
        if valid:
            images_formset.save()
        validated_forms_context = self.get_context_data(form=form, validated_images_form=images_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        art = Art.objects.get(pk=kwargs.get('pk'))
        art_form = ArtForm(data=request.POST, files=request.FILES, instance=art)
        images_formset = art_form.ImagesFormSet(request.POST, request.FILES, instance=art)
        return self.form_valid(art_form, images_formset)


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


def order_to_vendor(request, *args, **kwargs):
    order = Order.objects.get(pk=kwargs.get('pk'))
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
