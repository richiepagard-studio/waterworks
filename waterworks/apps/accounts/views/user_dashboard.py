import logging
from colorama import Fore, Style, init

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Configure logging for the accounts views module
logger = logging.getLogger(__name__)
init(autoreset=True)


class UserDashboardView(LoginRequiredMixin, View):
    """
    User dashboard view to handle users' dashboard.

    Methods:
        GET (HTTP).
    """
    template_name = "accounts/user_dashboard.html"

    def get(self, request):
        """
        Recognize the requested user by the 'request'
        and then render the dashboard template with user context.
        """
        user = request.user
        logger.info(
            f'User accessed dashboard: {Fore.LIGHTBLUE_EX}{user.username}{Style.RESET_ALL}'
        )

        context = {
            "section": "dashboard",
            "user": user
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
