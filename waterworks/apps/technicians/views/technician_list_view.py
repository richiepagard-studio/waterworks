from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.technicians.models import Technician
from apps.technicians.filters import TechnicianFilter


class TechnicianListView(LoginRequiredMixin, ListView):
    """
    List all active technicians.

    Methods:
        get(GET HTTP).
    """
    template_name = "technicians/technician_list.html"
    model = Technician
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        """
		Ensures that the user who creating a new user
		has an appropriate role.
		"""
        user = request.user
        is_allowed = (
            user.is_superuser
            or user.role == 'Admin'
        )

        # Redirects user only if user is neither
        # a superuser nor has an authorized role
        if not is_allowed:
            return redirect('accounts:user-dashboard')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns filtered queryset based on user role and search filters.
        """
        user = self.request.user

        # Base queryset based on role
        if user.role == "Technician":
            queryset = Technician.objects.filter(
                user_id=user.id
            )
        else:
            queryset = Technician.objects.filter(is_active=True)

        # Apply filtering
        self.filterset = TechnicianFilter(
            self.request.GET,
            queryset=queryset
        )

        return self.filterset.qs
