from apps.common.views import BaseRoleProfileUpdateView
from apps.technicians.models import Technician
from apps.technicians.forms import UpdateTechnicianForm


class TechnicianUpdateView(BaseRoleProfileUpdateView):
    model = Technician
    role = "Technician"
    form_class = UpdateTechnicianForm
    template_name = "technicians/technician_update.html"
