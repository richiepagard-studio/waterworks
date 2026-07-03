from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class UserLogoutView(View):
    """
    User logout view to handle users' logout.

    Methods:
        GET (HTTP).
    """
    def get(self, request):
        """
        Recognize the requested user by the 'request'
        and then logged it out.
        """
        logout(request)
        messages.success(
            request=request,
            message=_("You logged out to your account."),
            extra_tags="success"
        )
        return redirect('/')