from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.accounts.models import UserProfile


User = get_user_model()



class UserUpdateForm(forms.ModelForm):
    """
    Updating use info, not its profile.
    Important fields belongs to the User such as 'usernane'.
    """
    class Meta:
        model = User
        fields = ('username',)

        labels = {
            'username': _('نام کاربری')
        }


    def __init__(self, *args, **kwargs) -> None:
        """
        Initial fields and update their widget form.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-4'
            })


class UserProfileUpdateForm(forms.ModelForm):
    """
    Represent updating user profile.
    Just profile info.
    Validate the incoming data from the client and cleaned them.
    """

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'address')

        labels = {
            "first_name": _("نام کوچک"),
            "last_name": _("نام خانوادگی"),
            "address": _("آدرس")
        }


    def __init__(self, *args, **kwargs) -> None:
        """
        Initial fields and update their widget form.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mb-4'
            })
