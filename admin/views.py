from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from admin.mixins import IsAdminMixin
from admin.forms import UserForm, VendorForm, ArtistForm, ArtForm, SupportForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from vendor.models import Vendor, Shipping
from artist.models import Artist
from product.models import Art, Support, Stock, Colour, Size, Tag
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
        context = super(CreateUser, self).get_context_data(**kwargs)
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
        context = super(UpdateUser, self).get_context_data(**kwargs)
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
        context = super(CreateVendor, self).get_context_data(**kwargs)
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
        self.object = None
        return self.form_valid(vendor_form)


class UpdateVendor(IsAdminMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        context = super(UpdateVendor, self).get_context_data(**kwargs)
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
        self.object = self.get_object()
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
        if hasattr(self, 'object'):
            context['images_form'] = SupportForm.ProductImageFormSet(
                instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]

        # filter the colour and size options for current vendor
        curr_vend = Vendor.objects.get(id=self.kwargs['vendorid'])
        context['colours'] = Colour.objects.filter(vendor=curr_vend)
        context['sizes'] = Size.objects.filter(vendor=curr_vend)
        context['vendor_id'] = self.kwargs['vendorid']
        context['action'] = 'Create'
        return context

    def form_valid(self, support_form):
        if support_form.is_valid():
            redirect = super(CreateSupport, self).form_valid(support_form)
            #handle stock forms
            for field,val in support_form.data.items():
                if field.startswith('stock'):
                    stock_arr = field.split('_')
                    stock = Stock.objects.create(
                        colour_id=stock_arr[1],
                        size_id=stock_arr[2],
                        stock=val,
                        support=self.object
                    )
                    stock.save()
        else:
            validated_forms_context = self.get_context_data(form=support_form)
            redirect = self.render_to_response(validated_forms_context)

        return redirect

    def post(self, request, *args, **kwargs):
        support_form = SupportForm(data=request.POST)
        self.object = None
        return self.form_valid(support_form)


class UpdateSupport(IsAdminMixin, UpdateView):
    model = Support
    form_class = SupportForm
    template_name = 'admin/support/form.html'
    success_url = reverse_lazy('admin-supports')
    initial_product_image_data = [{'print_area':'{"x":100,"y":100,"width":250,"height":250}'}]

    def get_context_data(self, **kwargs):
        context = super(UpdateSupport, self).get_context_data(**kwargs)
        context['images_form'] = SupportForm.ProductImageFormSet(
            instance=self.object, initial=self.initial_product_image_data) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]
        # filter the colour and size options for current vendor
        context['colours'] = Colour.objects.filter(vendor=self.object.vendor)
        context['sizes'] = Size.objects.filter(vendor=self.object.vendor)
        context['stocks'] = self.get_grouped_stocks(context['colours'], context['sizes'])

        context['action'] = 'Update'
        context['vendor_id'] = self.object.vendor.id
        return context

    def get_grouped_stocks(self, colours, sizes):
        #arrange stocks by colours/sizes
        stocks_query = self.object.stock_set.order_by('colour', 'size').all()
        stocks = {}
        for stock in stocks_query:
            if stock.colour not in stocks:
                stocks[stock.colour] = {}
            stocks[stock.colour][stock.size] = {
                'stock':stock.stock,
                'id':stock.id
            }
        for colour in colours:
            if colour in stocks:
                for size in sizes:
                    if size not in stocks[colour]:
                        stocks[colour][size] = {
                            'stock': 0,
                            'id': 'new'
                        }
            else:
                stocks[colour] = {}
                for size in sizes:
                    stocks[colour][size] = {
                        'stock': 0,
                        'id': 'new'
                    }
        return stocks

    def form_valid(self, form):
        support = form.save()
        success_redirect = super(UpdateSupport, self).form_valid(form)
        #handle tabular stock forms
        for field, val in form.data.items():
            if field.startswith('stock'):
                stock_arr = field.split('_')
                if stock_arr[3] == 'new' and val != 0:
                    stock = Stock.objects.create(
                        colour_id=stock_arr[1],
                        size_id=stock_arr[2],
                        stock=val,
                        support=self.object
                    )
                    stock.save()
                else:
                    Stock.objects.filter(id=stock_arr[3]).update(stock=val)

        images_formset = form.ProductImageFormSet(self.request.POST, self.request.FILES, instance=support, initial=self.initial_product_image_data)
        valid = images_formset.is_valid()
        if valid:
            images_formset.save()
        validated_forms_context = self.get_context_data(form=form, validated_images_form=images_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        support = Support.objects.get(pk=kwargs.get('pk'))
        support_form = SupportForm(data=request.POST, instance=support)
        self.object = self.get_object()
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
        return super(VendorShippingCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendor = self.vendor
        return super(VendorShippingCreate, self).form_valid(form)


class VendorShippingDelete(IsAdminMixin, DeleteView):
    model = Shipping

    def get_success_url(self):
        return reverse_lazy('update-vendor', kwargs={'pk': self.object.vendor.id})


class CreateArtist(IsAdminMixin, CreateView):
    form_class = ArtistForm
    template_name = 'admin/artist/artist_form.html'
    success_url = reverse_lazy('admin-artists')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateArtist, self).get_context_data(**kwargs)
        context['title'] = 'Create Artist'
        context['submit_text'] = 'Create'
        return context


class UpdateArtist(IsAdminMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'admin/artist/artist_form.html'
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
        self.object = None
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
        # save newly created tags
        form.is_valid()
        form.cleaned_data['tags'] = []
        for tagId in form['tags'].data:
            try:
                tag = Tag.objects.get(id=tagId)
            except:
                tag = Tag(name=tagId)
                tag.save()
            form.cleaned_data['tags'].append(tag)
        # remove errors related to unexistant tags from form
        form._errors.pop('tags', None)
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
        self.object = self.get_object()
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


def order_to_vendor(request, order):
    context = {
        'order': order,
        'items': order.orderdetails_set.all(),
        'shipping': order.shippingdetails_set.first(),
        'base_url': 'https://' if request.is_secure() else 'http://' + request.get_host()
    }
    # return render(request, 'order/email/to_vendor/send_to_vendor.html', context)
    messageHtml = render_to_string('order/email/to_vendor/send_to_vendor.html', context)
    # send email to customer
    msg = EmailMultiAlternatives('Your order', body=messageHtml, from_email='noreply@tshirtstore.com',
                                 to=[order.vendor.email, ])
    msg.attach_alternative(messageHtml, "text/html")
    for bigImage in order.get_big_pictures():
        msg.attach_file(bigImage.path)
    msg.send()
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
