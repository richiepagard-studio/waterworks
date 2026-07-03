from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumber

from apps.accounts.models import User



class UserRegisterForm(forms.Form):
    """
    User registration form class.

    Handle user registration, its exceptions and validations.
    Validates matched passwords and valid phone-number.
    Validates the existence user with the phone-number.
    """
    phone_number = PhoneNumberField(
        region='IR',
        label=_('Phone number'),
        widget=forms.TextInput(attrs={'placeholder': 'شماره همراه مثل ۰۹۱۲۵۶۵۲۳۳۲'})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'رمزعبور'}),
        validators=[validate_password]
    )
    password_repeat = forms.CharField(
        label=_("Repeat your password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمزعبور'})
    )

    def __init__(self, *args, **kwargs):
        """
        Initialized the form class.

        Add some same widgets such as 'CSS class' to the all fields,
        or any other same properties.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-4',
                # "placeholder": field.label
            })

    def clean_phone(self):
        """
        Cleans the user phone-number.

        Gets the cleaned data (phone-number) and validate it
        if any user with that phone-number is already exists or not.
        """
        phone_number = self.cleaned_data.get('phone_number')

        # Check if the user with the phone-number is already exists
        if User.objects.filter(phone_number__iexact=phone_number).exists():
            # Add error if the user exists
            self.add_error(
                'phone_number',
                ValidationError(
                    _(
                        'You already have an account with this phone number.'
                        'You just need to login to your account.'
                    )
                )
            )

        return phone_number

    def clean(self):
        """
        General cleaning!

        Validates the password repeatition.
        Check if the passwords matched or not.
        """
        data = super().clean()

        # Clean passwords
        p1 = data.get('password')
        p2 = data.get('password_repeat')

        if p1 and p2 and p2 != p1:
            # Add validation error if the passwords do not match together
            self.add_error(
                'password',
                ValidationError(_('Passwords must match.'))
            )
