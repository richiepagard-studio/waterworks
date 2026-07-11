import logging
from colorama import Fore, Style, init

from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


# Configure logging for the accounts views module
logger = logging.getLogger(__name__)
init(autoreset=True)


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
        logger.info(
            f'User logged out successfully: {Fore.LIGHTYELLOW_EX}{request.user}{Style.RESET_ALL}'
        )

        return redirect('/')
