from django.urls import path

from .views import MainHomeView


app_name = "home"

urlpatterns = [
    path("", MainHomeView.as_view(), name="main-home")
]
