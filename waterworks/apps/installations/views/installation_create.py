from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.views import (
    BaseUserSoftRegisterView,
    BaseRoleProfileCreateView,
    BaseUserProfileSoftUpdateView
)
from apps.installations.forms import InstallationCreateForm


User = get_user_model()


class InstallationCreateUserView(BaseUserSoftRegisterView):
    """
    Creates a new user to create a new Installation base on the user object.
    Only the admin and technician roles be able to
    do this, creating a new Installation object means
    creating a new user with `Installation` role.
    """
    success_url = reverse_lazy("installations:installation-update-user-profile")
    template_name = "installations/installation_create_user.html"
    user_role = "Installation"
    authorized_roles = ("Admin", "Technician")


class InstallationUpdateUserProfileView(BaseUserProfileSoftUpdateView):
    """
    Updating and make created user's profile complete.
    User personal info, the user who has just created
    softly with the Installation role.
    """
    success_url = reverse_lazy("installations:installation-create")
    template_name = "installations/installation_update_user_profile.html"
    authorized_roles = ("Admin", "Technician")


class InstallationCreateView(BaseRoleProfileCreateView):
    """
    Creating a new Installation base on the user recently
    created with Installation role.
    Only users who authorized as Admin and Technician be able to do it.
    """
    form_class = InstallationCreateForm
    success_url = reverse_lazy("installations:installations-list")
    template_name = "installations/installation_create.html"
    user_role = "Installation"
    authorized_roles = ("Admin", "Technician")
