from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from admin.mixins import IsAdminMixin
from admin.forms import UserForm
from django.urls import reverse_lazy


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
