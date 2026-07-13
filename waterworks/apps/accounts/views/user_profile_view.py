import logging
from colorama import Fore, Style, init

from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.http import url_has_allowed_host_and_scheme

from apps.accounts.forms import UserUpdateForm, UserProfileUpdateForm


# Configure logging for the accounts views module
logger = logging.getLogger(__name__)
init(autoreset=True)

User = get_user_model()


class UserProfileUpdateView(View):
    """
    Updating user-profile.
    User's username and its profile information, too.
    Supporting two forms, one for user and one for profile info.

    Request:
        GET (HTTP).
        POST (HTTP).
    """
    form_classes = {
        "user_form": UserUpdateForm,
        "profile_form": UserProfileUpdateForm
    }
    template_name = "accounts/user_profile.html"
    authorized_roles: tuple[str, ...] = ("Admin",)

    def dispatch(self, *args, **kwargs):
        """
        Ensures that the user who creating a new user
        is one of the authorized users.
        """
        user = self.request.user
        is_allowed = (
            user.is_superuser
            or user.role in self.authorized_roles
            or user.id == self.kwargs.get("user_id")
        )
        logger.debug(
            f"{Fore.GREEN}Dispatching request for user: {user.username}, "
            f"Role: {user.role}, Is allowed: {is_allowed}{Style.RESET_ALL}"
        )

        if not is_allowed:
            logger.warning(
                f"{Fore.YELLOW}User {user.username} is not allowed to create a user profile.{Style.RESET_ALL}"
            )
            return redirect("home:main-home")

        return super().dispatch(*args, **kwargs)

    def _get_redirect_url(self, request) -> str:
        """
        Return a safe redirect target from the request or fall back to the dashboard.
        """
        redirect_to = (
            request.POST.get("next") or
            request.GET.get("next") or
            request.META.get("HTTP_REFERER")
        )

        if redirect_to and url_has_allowed_host_and_scheme(
            redirect_to,
            allowed_hosts={request.get_host()}
        ):
            return redirect_to

        return reverse_lazy("accounts:user-dashboard")

    def get(self, request, user_id=int) -> render:
        """
        Get the template and display it simply.

        Arguments:
            request: The HTTP request object.
            user_id: The ID of the user whose profile is being updated.
        """
        user = get_object_or_404(User, id=user_id)
        userprofile = user.userprofile
        context = {
            "user_form": self.form_classes["user_form"](instance=user),
            "profile_form": self.form_classes["profile_form"](instance=userprofile),
            "next_url": self._get_redirect_url(request),
        }

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request, user_id=int) -> render:
        """
        Validates forms by checking if the sent data
        from the client. If the data validated successfully,
        save the data as updating data for instances (user and userprofile).
        """
        user = get_object_or_404(User, id=user_id)
        userprofile = user.userprofile
        POST = request.POST
        forms = {
            "user_form": self.form_classes["user_form"](POST, instance=user),
            "profile_form": self.form_classes["profile_form"](POST, instance=userprofile)
        }
        redirect_url = self._get_redirect_url(request)

        # Check the validation of forms and
        # save them if they will validated properly
        if all(form.is_valid() for form in forms.values()):
            for form in forms.values():
                form.save()

            messages.success(
                request=request,
                message=_("پروفایل شما با موفقیت بروزرسانی شد."),
                extra_tags="success"
            )
            logger.info(
                f'User profile updated successfully: {Fore.LIGHTGREEN_EX}{user.username}{Style.RESET_ALL}'
            )

            return redirect(redirect_url)
        else:
            logger.error(
                f'Failed to update user profile: {Fore.LIGHTRED_EX}{user.username}{Style.RESET_ALL}'
            )
            messages.error(
                request=request,
                message=_("لطفا خطا زیر را بررسی و تصحیح کنید."),
                extra_tags="danger"
            )

        context = {
            **forms,
            "next_url": redirect_url,
        }

        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
