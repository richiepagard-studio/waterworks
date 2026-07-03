from django.urls import path

from apps.technicians.views import (
    # Creation
    TechnicianCreateUserView,
    TechnicianUpdateUserProfileView,
    TechnicianCreateView,
    # List and Retrieve
    TechnicianListView,
    TechnicianRetrieveView,
    # Update
    TechnicianUpdateView
)


app_name = "technicians"

TECHNICIAN_CRUD_URLS = [
    path(
        "create/user/",
        TechnicianCreateUserView.as_view(),
        name="technician-create-user"
    ),
    path(
        "user/profile/",
        TechnicianUpdateUserProfileView.as_view(),
        name="technician-update-user-profile"
    ),
    path("create/", TechnicianCreateView.as_view(), name="technician-create"),

    path("list/", TechnicianListView.as_view(), name="technicians-list"),
    path("<int:technician_pk>/", TechnicianRetrieveView.as_view(), name="technician-retrieve"),

    path("<int:instance_pk>/update/", TechnicianUpdateView.as_view(), name="technician-update"),
]

urlpatterns = TECHNICIAN_CRUD_URLS
