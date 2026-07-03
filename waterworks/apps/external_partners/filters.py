from django.forms import TextInput

import django_filters

from apps.external_partners.models import Vendor


class VendorFilter(django_filters.FilterSet):
    """
    Search filter on vendors.
    """
    shop_name = django_filters.CharFilter(
        widget=TextInput(attrs={"class": "form-control"})
    )
    contact_phone = django_filters.CharFilter(
        widget=TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Vendor
        fields = ("shop_name", "contact_phone")
