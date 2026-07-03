from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Device


class DeviceCreateForm(forms.ModelForm):
    """
    The creation of the device model.
    """
    class Meta:
        model = Device
        fields = (
            'name',
            'model',
            'guarantee',
            'stock_quantity',
            'is_in_stock',
            'image'
        )

        labels = {
            'name': _('نام دستگاه'),
            'model': _('مدل دستگاه'),
            'guarantee': _('گارانتی دستگاه'),
            'stock_quantity': _('موجودی'),
            'is_in_stock': _('وضعیت موجودی'),
            'image': _('تصویر بنر دستگاه')
        }

        widgets = {
            'is_in_stock': forms.CheckboxInput(attrs={'type': 'checkbox'}),
        }


    def __init__(self, *args, **kwargs):
        """
        Initialized the form class.

        Add some same widgets such as 'CSS class' to the all fields,
        or any other same properties.
        """
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input mb-3'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control mb-3',
                    'placeholder': field.help_text
                })


class DeviceUpdateForm(forms.ModelForm):
    """
    Custom updating form for device update view.
    """
    class Meta:
        model = Device
        fields = [
            'name', 'model', 'installed_count', 'guarantee',
            'stock_quantity', 'is_in_stock', 'description', 'image'
        ]

        labels = {
            'name': _('نام دستگاه'),
            'model': _('مدل دستگاه'),
            'guarantee': _('گارانتی دستگاه'),
            'stock_quantity': _('موجودی'),
            'is_in_stock': _('وضعیت موجودی'),
            'image': _('تصویر حال حاضر')
        }

    def __init__(self, *args, **kwargs):
        """
        Initialized the form class.

        Add some same widgets such as 'CSS class' to the all fields,
        or any other same properties.
        """
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input mb-3'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control mb-3',
                    'placeholder': field.help_text
                })

    def clean_stock_quantity(self) -> int:
        """
        Validating the stock-quantity value to not being negative.
        """
        value = self.cleaned_data['stock_quantity']
        if value < 0:
            raise forms.ValidationError(_('موجودی نمی‌تواند منفی باشد.'))
        return value

    def clean(self) -> dict:
        """
        Validating the whole form logic.

        Validates if a stock-quantity is 0 and the in-stock
        is True, raise an error to say the device cannot be
        in stock when its quantity is 0.
        """
        cleaned_data = super().clean()
        stock_quantity = cleaned_data.get('stock_quantity')
        is_in_stock = cleaned_data.get('is_in_stock')

        if stock_quantity == 0 and is_in_stock:
            self.add_error('is_in_stock', _('وقتی موجودی صفر است، دستگاه نباید موجود باشد.'))

        return cleaned_data
