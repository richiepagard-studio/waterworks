from django.urls import path

from apps.external_partners.views import (
    # Creation
    VendorCreateUserView,
    VendorUpdateUserProfileView,
    VendorCreateView,
    # List and retrieve
    VendorListView,
    VendorRetrieveView,
    # Updating
    VendorUpdateView
)

app_name = "external_partners"

VENDORS_CRUD_URLS = [
    # Creation
    path(
        "create/user/",
        VendorCreateUserView.as_view(),
        name="vendor-create-user"
    ),
    path(
        "user/profile/",
        VendorUpdateUserProfileView.as_view(),
        name="vendor-update-user-profile"
    ),
    path(
        "create/",
        VendorCreateView.as_view(),
        name="vendor-create"
    ),
    # Updating
    path(
        "<int:instance_pk>/update/",
        VendorUpdateView.as_view(),
        name="vendor-update"
    ),
    # List and retrieve
    path("list/", VendorListView.as_view(), name="vendors-list"),
    path("<int:vendor_pk>/", VendorRetrieveView.as_view(), name="vendor-retrieve"),
]

urlpatterns = VENDORS_CRUD_URLS
