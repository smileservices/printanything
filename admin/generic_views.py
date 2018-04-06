from django.views import generic
from admin.mixins import IsAdminMixin


class ListView(IsAdminMixin, generic.ListView):
    pass


class DeleteView(generic.DeleteView, IsAdminMixin):
    pass
