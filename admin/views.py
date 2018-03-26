from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin
from admin.forms import UserForm, VendorForm, ArtistForm, ArtForm, BaseImageFormSet
from django.urls import reverse_lazy
from vendor.models import Vendor
from artist.models import Artist
from product.models import Art, Support


def dashboard(request):
    if request.user.is_staff:
        return render(request, 'admin/dashboard.html')
    else:
        return redirect('login')


class CreateUser(LoginRequiredMixin, CreateView):
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


class UpdateUser(LoginRequiredMixin, UpdateView):
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


class CreateVendor(LoginRequiredMixin, CreateView):
    form_class = VendorForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Vendor'
        context['submit_text'] = 'Create'
        return context


class UpdateVendor(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Vendor'
        context['submit_text'] = 'Update'
        context['supports'] = self.object.support_set.all()
        return context


class CreateSupport(LoginRequiredMixin, CreateView):
    model = Support


class UpdateSupport(LoginRequiredMixin, UpdateView):
    model = Support


class CreateArtist(LoginRequiredMixin, CreateView):
    form_class = ArtistForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Artist'
        context['submit_text'] = 'Create'
        return context


class UpdateArtist(LoginRequiredMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'admin/vendor/vendor_form.html'
    success_url = reverse_lazy('admin-artists')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Artist'
        context['submit_text'] = 'Update'
        return context


class CreateArt(LoginRequiredMixin, CreateView):
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-vendors')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Art'
        context['submit_text'] = 'Art'
        return context


class UpdateArt(LoginRequiredMixin, UpdateView):
    model = Art
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-art')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Art'
        context['submit_text'] = 'Update'
        context['images_form'] = ArtForm.ImagesFormSet(instance=self.object) if "validated_images_form" not in kwargs else kwargs["validated_images_form"]
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
        art_form = ArtForm(data=request.POST, instance=art)
        images_formset = art_form.ImagesFormSet(request.POST, request.FILES, instance=art)
        return self.form_valid(art_form, images_formset)
