from typing import Any
from django.forms import Select, TextInput

import django_filters
from phonenumber_field.phonenumber import PhoneNumber

from apps.devices.models import Device
from apps.technicians.models import Technician
from apps.external_partners.models import Vendor
from apps.installations.models import Installation


class InstallationFilter(django_filters.FilterSet):
    """
    Search filter on installations.
    """
    device = django_filters.ModelChoiceFilter(
        queryset=Device.objects.filter(is_active=True),
        widget=Select(attrs={"class": "form-control"})
    )
    technician = django_filters.ModelChoiceFilter(
        queryset=Technician.objects.filter(is_active=True),
        widget=Select(attrs={"class": "form-control"})
    )
    vendor = django_filters.ModelChoiceFilter(
        queryset=Vendor.objects.filter(is_active=True),
        widget=Select(attrs={"class": "form-control"})
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
        model = Installation
        fields = (
            "device",
            "technician",
            "vendor",
            "first_name",
            "last_name",
            "phone_number"
        )

    def __init__(self, *args, **kwargs):
        request = kwargs.get("request")
        super().__init__(*args, **kwargs)

        if not request:
            return

        user = request.user

        # Technician cannot filter by technician
        if user.role == "Technician":
            self.filters.pop("technician", None)

        # Vendor cannot filter by vendor
        if user.role == "Vendor":
            self.filters.pop("vendor", None)

    def filter_phone_number(self, queryset: Any, name: str, value: str) -> Any:
        """
        Filter installations by a partial phone number.

        The phone number is stored in the database in its normalized
        international format, while the user may enter either a local
        Iranian number or an international number. This method converts
        the input to a searchable representation and performs a partial
        match using PostgreSQL's ILIKE lookup.
        """
        value = value.strip()

        if not value:
            return value

        if value.startswith("0"):
            value = "+98" + value[1:]
        elif value.startswith("98"):
            value = "+" + value
        elif not value.startswith("+"):
            value = "+98" + value

        return queryset.filter(
            user__phone_number__icontains=value
        )
