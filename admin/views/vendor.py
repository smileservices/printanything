from django.views.generic.edit import CreateView, UpdateView
from admin.mixins import IsAdminMixin
from admin.forms import VendorForm
from django.urls import reverse_lazy
from vendor.models import Vendor


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
