from django.views.generic.edit import CreateView, UpdateView, DeleteView
from admin.mixins import IsAdminMixin
from django.urls import reverse_lazy
from admin.forms import ApiInterfaceForm
from api_interface.models import ApiInterface

class Create(IsAdminMixin, CreateView):
    form_class = ApiInterfaceForm
    template_name = 'admin/api_interface/form.html'
    success_url = reverse_lazy('admin-api_interface')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Create, self).get_context_data(**kwargs)
        context['title'] = 'Create '
        context['submit_text'] = 'Create'
        return context


class Update(IsAdminMixin, UpdateView):
    model = ApiInterface
    form_class = ApiInterfaceForm
    template_name = 'admin/api_interface/form.html'
    success_url = reverse_lazy('admin-api_interface')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update '
        context['submit_text'] = 'Update'
        return context
