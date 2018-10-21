from django.views.generic.edit import CreateView, UpdateView
from admin.mixins import IsAdminMixin
from admin.forms import ArtForm
from django.urls import reverse_lazy
from product.models import Art, Tag


class CreateArt(IsAdminMixin, CreateView):
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-art')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Art'
        context['submit_text'] = 'Create'
        return context

    def post(self, request, *args, **kwargs):
        form = ArtForm(data=request.POST, files=request.FILES)
        form.is_valid()  # we need to run this in order to access cleaned_data. yeah. django forms sucks ass!
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
        self.object = None
        return self.form_valid(form)


class UpdateArt(IsAdminMixin, UpdateView):
    model = Art
    form_class = ArtForm
    template_name = 'admin/art/art_form.html'
    success_url = reverse_lazy('admin-art')

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Art'
        context['submit_text'] = 'Update'
        return context

    def post(self, request, *args, **kwargs):
        art = Art.objects.get(pk=kwargs.get('pk'))
        form = ArtForm(data=request.POST, files=request.FILES, instance=art)
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
        self.object = self.get_object()
        return self.form_valid(form)
