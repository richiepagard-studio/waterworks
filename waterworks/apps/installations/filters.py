from typing import Any
from django.forms import Select, TextInput
from django.utils.translation import gettext_lazy as _

import django_filters
from phonenumber_field.phonenumber import PhoneNumber
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from apps.devices.models import Device
from apps.technicians.models import Technician
from apps.external_partners.models import Vendor
from apps.installations.models import Installation


class JalaliDateFilter(django_filters.DateFilter):
    """
    DateFilter that accepts Jalali dates and converts them
    to Gregorian for filtering, reusing the project's Jalali
    date field/widget.
    """
    field_class = JalaliDateField


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

    start_date = JalaliDateFilter(
        field_name="installation_date",
        lookup_expr="gte",
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "placeholder": _("از تاریخ"),
            "autocomplete": "off",
        })
    )
    end_date = JalaliDateFilter(
        field_name="installation_date",
        lookup_expr="lte",
        widget=AdminJalaliDateWidget(attrs={
            "class": "form-control jalali_date-date",
            "placeholder": _("تا تاریخ"),
            "autocomplete": "off",
        })
    )

    class Meta:
        model = Installation
        fields = (
            "device",
            "technician",
            "vendor",
            "first_name",
            "last_name",
            "phone_number",
            # Dates range
            "start_date",
            "end_date"
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
