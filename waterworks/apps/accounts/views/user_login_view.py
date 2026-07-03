from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import UserLoginForm


class UserLoginView(View):
    """
    Handle user login and authorization.

    Methods:
        GET (HTTP).
        POST (HTTP).
    """
    form_class = UserLoginForm
    template_name = "accounts/user_login.html"

    def get(self, request):
        """
        Just shows the form and everything in the context.
        """
        form = self.form_class

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):
        """
        Post http method to get client account info,
        validate the form data and then authenticate the user.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(
                username=cleaned_data.get("phone_number"),
                password=cleaned_data.get("password")
            )

            if user is not None:
                login(request=request, user=user)
                messages.success(
                    request=request,
                    message=_("You logged in successfully."),
                    extra_tags="success"
                )
                return redirect("/")
            else:
                messages.error(
                    request=request,
                    message=_("Your phone number or password was wrong. Try again."),
                    extra_tags="danger"
                )

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
