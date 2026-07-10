from django.shortcuts import redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apps.installations.models import Installation


class InstallationDetailView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DetailView
):
    """
    Retrieve and display the details of a single Installation.

    This view serves the installation detail endpoint and renders
    the installation information based on the user's role and
    access permissions.

    Access control is enforced to ensure that only authorized users
    can view the installation record. The queryset is restricted
    according to the authenticated user's role.

    Methods:
		test_func()
			Validates whether the current user has permission to access
			the view based on their role.

		handle_no_permission()
			Redirects unauthorized users to the user dashboard.

		get_queryset()
			Returns a filtered queryset of installations according to
			the authenticated user's role.
    """

    model = Installation
    pk_url_kwarg = "installation_pk"

    def test_func(self):
        """
        Determine whether the authenticated user has permission
        to access this view.

        The permission check allows access for:
			- Superusers
			- Admin users
			- Technicians
			- Vendors
			- Customers

        Returns:
			bool
				True if the user has an authorized role, otherwise False.
        """
        user = self.request.user
        return (
            user.is_superuser
            or user.role in ["Admin", "Technician", "Vendor", "Customer"]
        )

    def handle_no_permission(self):
        """
        Handle requests from users who fail the permission test.

        Instead of returning a 403 response, the user is redirected
        to the main user dashboard.

        Returns:
			HttpResponseRedirect
				Redirect response to the user dashboard page.
        """
        return redirect("accounts:user-dashboard")

    def get_queryset(self):
        """
        Return a role-restricted queryset of Installation objects.

        The queryset is filtered to ensure that users only access
        installations related to their role:

        - Technicians can only see installations assigned to them.
        - Vendors can only see installations associated with them.
        - Customers can only see their own installations.
        - Admins and superusers can access all installations.

        Returns:
			QuerySet
				A filtered queryset of Installation objects based on
				the current user's role.
        """
        user = self.request.user

        if user.role == "Technician":
            return Installation.objects.filter(
                technician__user=user
            )

        elif user.role == "Vendor":
            return Installation.objects.filter(
                vendor__user=user
            )

        elif user.role == "Customer":
            return Installation.objects.filter(
                user=user
            )

		# Admin / superuser
        return Installation.objects.all()
