from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _


class UserSoftRegisterForm(forms.Form):
    """
    User registration form.

    Only validates user input.
    User creation and registration logic are handled
    in the service layer.
    """

    phone_number = forms.CharField(
        label=_('شماره همراه'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('شماره همراه مثل ۰۹۱۲۵۶۵۲۳۳۲')
            }
        )
    )

    password = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('رمز عبوری را وارد کنید')
            }
        )
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize form widgets and attributes.
        """
        super().__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs.update(
            {
                'class': 'mb-4',
                'dir': 'rtl',
            }
        )

        self.fields['password'].widget.attrs.update(
            {
                'class': 'mb-4',
            }
        )

    def clean_password(self) -> str:
        """
        Validate password strength using Django's
        built-in password validators.
        """

        password = self.cleaned_data['password']

        try:
            validate_password(password)

        except ValidationError as validation_error:
            raise forms.ValidationError(
                validation_error.messages
            )

        return password
