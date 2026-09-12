from typing import Any
from django.forms import TextInput

import django_filters
from phonenumber_field.phonenumber import PhoneNumber

from apps.external_partners.models import Vendor


class VendorFilter(django_filters.FilterSet):
    """
    Search filter on vendors.
    """
    shop_name = django_filters.CharFilter(
        field_name="shop_name",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"})
    )
    contact_phone = django_filters.CharFilter(
        field_name="contact_phone",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"})
    )
    first_name = django_filters.CharFilter(
        field_name="user__userprofile__first_name",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"})
    )
    last_name = django_filters.CharFilter(
        field_name="user__userprofile__last_name",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"})
    )
    phone_number = django_filters.CharFilter(
        field_name=str("user__phone_number"),
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Vendor
        fields = (
            "shop_name",
            "contact_phone",
            "first_name",
            "last_name",
            "phone_number"
        )


    def filter_phone_number(self, queryset: Any, name: str, value: str) -> Any:
        value = value.strip()

        if not value:
            return value

        return queryset.filter(
            user__phone_number__icontains=value
        )
