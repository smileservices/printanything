from django.views.generic.edit import CreateView, UpdateView
from admin.mixins import IsAdminMixin
from admin.forms import ArtistForm
from django.urls import reverse_lazy
from artist.models import Artist


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
