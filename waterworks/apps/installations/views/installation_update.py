from django.urls import reverse_lazy

from apps.common.views import BaseRoleProfileUpdateView
from apps.installations.models import Installation
from apps.installations.forms import InstallationUpdateForm


class InstallationUpdateView(BaseRoleProfileUpdateView):
    model = Installation
    role = "Customer"
    form_class = InstallationUpdateForm
    template_name = "installations/installation_update.html"
