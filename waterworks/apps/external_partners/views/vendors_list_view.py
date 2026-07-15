from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.external_partners.models import Vendor
from apps.external_partners.filters import VendorFilter


class VendorListView(LoginRequiredMixin, ListView):
    """
    List all vendors.

    Methods
        get(GET HTTP).
    """
    template_name = "external_partners/vendor_pages/vendors_list.html"
    model = Vendor
    paginate_by = 9

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

    def get_queryset(self):
        """
        Returns filtered queryset based on user role and search filters.
        """
        queryset = Vendor.objects.all()

        # Apply filtering
        self.filterset = VendorFilter(
            self.request.GET,
            queryset=queryset
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Adds the filterset to the context for rendering in the template.
        """
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
