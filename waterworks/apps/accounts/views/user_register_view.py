from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import UserRegisterForm
from apps.accounts.models import User


class UserRegisterView(View):
    """
    User registration view, handle users' registration.

    Methods:
        GET (HTTP).
        POST (HTTP).
    """
    form_class = UserRegisterForm
    template_name = "accounts/user_register.html"

    def get(self, request):
        """
        Just shows the template and its form.
        Or eveything in 'context'.
        """
        form = self.form_class()

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):
        """
        Register users by validate the form data.
        Create a rudimentary user with 'phone-number' and 'password'.
        Redirect user to the login page if the registration done successfully.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                phone_number = data.get("phone_number"),
                password=data.get("password")
            )
            user.save()
            messages.success(
                request=request,
                message=_("Your account registration was successfully done."),
                extra_tags="success"
            )
            return redirect("accounts:user-login")
        else:
            form.errors

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
