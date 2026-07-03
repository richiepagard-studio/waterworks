from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from apps.installations.models import Installation
from apps.technicians.models import Technician
from apps.external_partners.models import Vendor
from apps.devices.models import Device


class MainHomeView(TemplateView):
    """
    Renders the main home page template with
    the custom contexts.

    Methods:
        get_context_data: Defines custom context.
    """
    template_name =  "home/main_home.html"

    def get_context_data(self, **kwargs):
        """
        Lists of last objects from the selected model.
        List the count of all roles and devices.
        """
        context = super().get_context_data(**kwargs)

        # List of last objects
        context['last_five_installations'] = Installation.last_objects(5)
        context['last_three_devices'] = Device.most_installation(3)

        # Number of objects
        context['installations_count'] = Installation.objects.count()
        context['technicians_count'] = Technician.objects.count()
        context['vendors_count'] = Vendor.objects.count()
        context['devices_count'] = Device.objects.count()

        return context
