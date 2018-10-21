from django.views.generic.edit import CreateView, UpdateView
from admin.mixins import IsAdminMixin
from admin.forms import SupportForm
from django.urls import reverse_lazy
from vendor.models import Vendor
from product.models import Support, Stock, Colour, Size


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
            # handle stock forms
            for field, val in support_form.data.items():
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
    initial_product_image_data = [{'print_area': '{"x":100,"y":100,"width":250,"height":250}'}]

    def get_context_data(self, **kwargs):
        context = super(UpdateSupport, self).get_context_data(**kwargs)
        context['images_form'] = SupportForm.ProductImageFormSet(
            instance=self.object, initial=self.initial_product_image_data) if "validated_images_form" not in kwargs else \
        kwargs["validated_images_form"]
        # filter the colour and size options for current vendor
        context['colours'] = Colour.objects.filter(vendor=self.object.vendor)
        context['sizes'] = Size.objects.filter(vendor=self.object.vendor)
        context['stocks'] = self.get_grouped_stocks(context['colours'], context['sizes'])

        context['action'] = 'Update'
        context['vendor_id'] = self.object.vendor.id
        return context

    def get_grouped_stocks(self, colours, sizes):
        # arrange stocks by colours/sizes
        stocks_query = self.object.stock_set.order_by('colour', 'size').all()
        stocks = {}
        for stock in stocks_query:
            if stock.colour not in stocks:
                stocks[stock.colour] = {}
            stocks[stock.colour][stock.size] = {
                'stock': stock.stock,
                'id': stock.id
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
        # handle tabular stock forms
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

        images_formset = form.ProductImageFormSet(self.request.POST, self.request.FILES, instance=support,
                                                  initial=self.initial_product_image_data)
        valid = images_formset.is_valid()
        if valid:
            # cycle through all images and make sure only one is primary
            primary = False
            for i, form in enumerate(images_formset):
                if form.instance.primary == True and not primary:
                    primary = True
                elif primary:
                    form.instance.primary = False
            if not primary:
                images_formset[0].instance.primary = True
            images_formset.save()

        validated_forms_context = self.get_context_data(form=form, validated_images_form=images_formset)
        return success_redirect if valid else self.render_to_response(validated_forms_context)

    def post(self, request, *args, **kwargs):
        support = Support.objects.get(pk=kwargs.get('pk'))
        support_form = SupportForm(data=request.POST, instance=support)
        self.object = self.get_object()
        return self.form_valid(support_form)
