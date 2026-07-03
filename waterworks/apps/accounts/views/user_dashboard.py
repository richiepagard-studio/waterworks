from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class UserDashboardView(LoginRequiredMixin, View):
    template_name = "accounts/user_dashboard.html"

    def get(self, request):
        user = request.user

        context = {
            "section": "dashboard",
            "user": user
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
