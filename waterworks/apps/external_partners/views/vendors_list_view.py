from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.external_partners.models import Vendor
from apps.external_partners.filters import VendorFilter


class VendorListView(LoginRequiredMixin, View):
    """
    List all vendors.

    Methods
        get(GET HTTP).
    """
    template_name = "external_partners/vendor_pages/vendors_list.html"

    def dispatch(self, *args, **kwargs):
        """
        Ensures that the user who seeing the list of vendors,
        has an appropriate permissions/role.
        """
        user = self.request.user
        is_allowed = (
            user.is_superuser
            or user.role in ("Admin",)
        )

        # Redirects user only if user is neither
        # a superuser nor has an authorized role
        if not is_allowed:
            return redirect("home:main-home")

        return super().dispatch(*args, **kwargs)

    def get(self, request):
        """
        Lists all the vendors,
        filters them base on the client request, the search filter.
        """
        vendors = Vendor.objects.all()
        # Search filter according to the 'VendorFilter'
        filters = VendorFilter(
            request.GET,
            queryset=Vendor.objects.all()
        )
        # Remake the quesryset to the requests of the search filters
        vendors = filters.qs

        context = {
            "vendors": vendors,
            "filters": filters
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
