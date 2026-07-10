from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.technicians.models import Technician
from apps.technicians.filters import TechnicianFilter


class TechnicianListView(LoginRequiredMixin, View):
    """
    List all active technicians.

    Methods:
        get (GET HTTP).
    """
    template_name = "technicians/technician_list.html"

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

    def get(self, request):
        """
        Gets all active technicians and list them.
        """
        technicians = Technician.objects.filter(is_active=True)
        # Search filter according to the 'TechnicianFilter'
        filters = TechnicianFilter(request.GET, queryset=Technician.objects.all())
        # Remake the quesryset to the requests of the search filters
        technicians = filters.qs

        context = {
            "technicians": technicians,
            "filters": filters
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
