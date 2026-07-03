from django.urls import path

from apps.installations.views import (
    # Creation
    InstallationCreateUserView,
    InstallationUpdateUserProfileView,
    InstallationCreateView,
    # Updating
    InstallationUpdateView,
    # List and retrieve
    InstallationListView,
    InstallationDetailView
)

app_name = "installations"

INSTALLATION_CRUD_URLS = [
    # Creations
    path(
        "create/user/",
        InstallationCreateUserView.as_view(),
        name="installation-create-user"
    ),
    path(
        "user/profile/",
        InstallationUpdateUserProfileView.as_view(),
        name="installation-update-user-profile"
    ),
    path("create/", InstallationCreateView.as_view(), name="installation-create"),

    # Updating
    path(
        "<int:instance_pk>/update/",
        InstallationUpdateView.as_view(),
        name="installation-update"
    ),

    # List and Retrieve
    path("list/", InstallationListView.as_view(), name="installations-list"),
    path("<int:installation_pk>/", InstallationDetailView.as_view(), name="installation-retrieve")
]

urlpatterns = INSTALLATION_CRUD_URLS
