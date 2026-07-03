from django.urls import path

from apps.accounts.views import (
    UserLoginView,
    UserRegisterView,
    UserLogoutView,
    # User Profile
    UserProfileUpdateView,
    UserDashboardView,
)


app_name = 'accounts'

AUTHENTICATION_URLS = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
]
USER_PROFILE_URLS = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('dashboard/', UserDashboardView.as_view(), name='user-dashboard')
]

urlpatterns = AUTHENTICATION_URLS + USER_PROFILE_URLS
