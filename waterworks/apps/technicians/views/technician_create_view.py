from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.common.views import (
    BaseUserSoftRegisterView,
    BaseUserProfileSoftUpdateView,
    BaseRoleProfileCreateView
)
from apps.technicians.forms import CreateTechnicianForm
from apps.technicians.models import Technician


class TechnicianCreateUserView(BaseUserSoftRegisterView):
    """
    Creates a new user to create a new technician base on the user object.
    Only the admin role be able to do this,
    creating a new technician object means creating a new user with `Technician` role.
    """
    success_url = reverse_lazy("technicians:technician-update-user-profile")
    template_name = "technicians/technician_create_user.html"
    user_role = "Technician"
    authorized_roles = ("Admin",)


class TechnicianUpdateUserProfileView(BaseUserProfileSoftUpdateView):
    """
    Updating and make created user's profile complete.
    User personal info, the user who has just created
    softly with the Technician role.
    """
    success_url = reverse_lazy("technicians:technician-create")
    template_name = "technicians/technician_update_user_profile.html"
    authorized_roles = ("Admin",)


class TechnicianCreateView(BaseRoleProfileCreateView):
    """
    Creating a new technician base on the user recently
    created with Technician role.
    Only users who authorized as Admin be able to do it.
    """
    success_url = reverse_lazy("technicians:technicians-list")
    form_class = CreateTechnicianForm
    template_name = "technicians/technician_create.html"
    user_role = "Technician"
    authorized_roles = ("Admin",)
