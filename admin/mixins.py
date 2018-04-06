from braces.views import LoginRequiredMixin


class IsAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission(request)
        return super(IsAdminMixin, self).dispatch(
            request, *args, **kwargs)
