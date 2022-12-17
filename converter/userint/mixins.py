from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginRequiredRedirectMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        return super().dispatch(request, *args, **kwargs)
