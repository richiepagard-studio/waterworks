from django.urls import reverse_lazy

from apps.common.views import (
    BaseUserSoftRegisterView,
    BaseUserProfileSoftUpdateView,
    BaseRoleProfileCreateView
)
from apps.external_partners.forms import VendorCreateForm


class VendorCreateUserView(BaseUserSoftRegisterView):
    """
    Creates a new user to create a new vendor base on the user object.
    Only the admin role be able to
    do this, creating a new vendor object means
    creating a new user with `Vendor` role.
    """
    success_url = reverse_lazy("external_partners:vendor-update-user-profile")
    template_name = "external_partners/vendor_pages/vendor_create_user.html"
    user_role = "Vendor"
    authorized_roles = ("Admin",)


class VendorUpdateUserProfileView(BaseUserProfileSoftUpdateView):
    """
    Updating and make created user's profile complete.
    User personal info, the user who has just created
    softly with the Vendor role.
    """
    success_url = reverse_lazy("external_partners:vendor-create")
    template_name = "external_partners/vendor_pages/vendor_update_user_profile.html"
    authorized_roles = ("Admin",)


class VendorCreateView(BaseRoleProfileCreateView):
    """
    Creating a new vendor base on the user recently
    created with Vendor role.
    Only users who authorized as Admin is be able to do it.
    """
    form_class = VendorCreateForm
    success_url = reverse_lazy("external_partners:vendors-list")
    template_name = "external_partners/vendor_pages/vendor_create.html"
    user_role = "Vendor"
    authorized_roles = ("Admin",)
