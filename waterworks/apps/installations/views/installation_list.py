from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.installations.models import Installation
from apps.installations.filters import InstallationFilter


class InstallationListView(LoginRequiredMixin, ListView):
    """
    List all installations.

    Methods
        get(GET HTTP).
    """
    model = Installation
    paginate_by = 1


    def dispatch(self, request, *args, **kwargs):
        """
        Ensures that the user who creating a new user
        has an appropriate role.
        """
        user = request.user
        if user.is_authenticated:
            is_allowed = (
                user.is_superuser
                or user.role == 'Admin'
                or user.role == 'Technician'
                or user.role == 'Vendor'
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
            queryset = Installation.objects.filter(
                technician__user_id=user.id
            )
        elif user.role == "Vendor":
            queryset = Installation.objects.filter(
                vendor__user_id=user.id
            )
        else:
            queryset = Installation.objects.filter(is_active=True)

        # Apply django-filter
        self.filterset = InstallationFilter(
            self.request.GET,
            queryset=queryset,
            request=self.request
        )

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Inject filterset into template context.
        """
        context = super().get_context_data(**kwargs)
        context["filters"] = self.filterset

        return context
