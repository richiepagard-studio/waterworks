from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from apps.accounts.forms import UserUpdateForm, UserProfileUpdateForm


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

    def get(self, request):
        """
        Get the template and display it simply.
        """
        user = request.user
        userprofile = user.userprofile
        forms = {
            "user_form": self.form_classes["user_form"](instance=user),
            "profile_form": self.form_classes["profile_form"](instance=userprofile)
        }

        return render(
            request=request,
            template_name=self.template_name,
            context=forms
        )

    def post(self, request):
        """
        Validates forms by checking if the sent data
        from the client. If the data validated successfully,
        save the data as updating data for instances (user and userprofile).
        """
        user = request.user
        userprofile = user.userprofile
        POST = request.POST
        forms = {
            "user_form": self.form_classes["user_form"](POST, instance=user),
            "profile_form": self.form_classes["profile_form"](POST, instance=userprofile)
        }

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
            return redirect(reverse_lazy("accounts:user-dashboard"))
        else:
            messages.error(
                request=request,
                message=_("لطفا خطا زیر را بررسی و تصحیح کنید."),
                extra_tags="danger"
            )
        return render(
            request=request,
            template_name=self.template_name,
            context=forms
        )
