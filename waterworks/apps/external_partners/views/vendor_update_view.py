from django.urls import reverse_lazy

from apps.common.views import BaseRoleProfileUpdateView
from apps.external_partners.models import Vendor
from apps.external_partners.forms import VendorUpdateForm


class VendorUpdateView(BaseRoleProfileUpdateView):
    model = Vendor
    role = "Vendor"
    form_class = VendorUpdateForm
    template_name = "external_partners/vendor_pages/vendor_update.html"
