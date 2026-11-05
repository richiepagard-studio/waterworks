from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from apps.common.views import BaseRoleProfileUpdateView
from apps.external_partners.models import Vendor
from apps.external_partners.forms import VendorUpdateForm


class VendorUpdateView(UpdateView):
    """
    Updating the vendor profile info.
    Just the admin users and the profile owner be able to edit the profile.
    """
    model = Vendor
    form_class = VendorUpdateForm
    template_name = "external_partners/vendor_pages/vendor_update.html"
    pk_url_kwarg = "vendor_pk"
    success_url = reverse_lazy("home:main-home")

    def dispatch(self, *args, **kwargs):
        """
        Ensures that the user who updating a profile has the Admin role,
        superuser role, or the owner of the profile.
        Checking the privilege.
        """
        user = self.request.user
        vendor = self.get_object()
        is_allowed = (
            user.is_superuser or user.role == "Admin"
            or user == vendor.user
        )

        if not is_allowed:
            return redirect("home:main-home")

        return super().dispatch(*args, **kwargs)
