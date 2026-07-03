from django import forms
from django.utils.translation import gettext_lazy as _



class UserLoginForm(forms.Form):
    """
    User login form.

    Attributes:
        phone_number (str): Authenticate user with phone number as a USERNAME field.
        password (str): User's password with PasswordInput widget for saftly.
    """
    phone_number = forms.CharField(
        min_length=11,
        max_length=13,
        required=True,
        label=_('شماره همراه')
    )
    password = forms.CharField(
        label=_('رمز عبور'),
        widget=forms.PasswordInput
    )

    labels = {
        'phone_number': _('شماره همراه'),
        'password': _('رمز عبور'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholder for fields
        self.fields['phone_number'].widget.attrs = {
            'placeholder': _('شماره همراه مثل ۰۹۱۲۵۶۵۲۳۳۲'),
            'class': 'mb-4',
        }
        self.fields['password'].widget.attrs = {
            'placeholder': _('رمزعبور'),
            'class': 'mb-4',
        }

        # Get the placeholders to use them in the template fields' placeholders
        self.password_placeholder = self.fields['password'].widget.attrs.get('placeholder')
        self.phone_number_placeholder = self.fields['phone_number'].widget.attrs.get('placeholder')
