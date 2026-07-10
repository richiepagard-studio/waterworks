from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.forms import Form, ModelForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from apps.accounts.forms import UserSoftRegisterForm, UserProfileUpdateForm
from apps.accounts.models import UserProfile
from apps.accounts.service import register_or_continue_user


User = get_user_model()


class BaseUserSoftRegisterView(LoginRequiredMixin, View):
    """
    Registering a new user by a more soft way.
    Only use for views that will create a new user
    with a special Role (e.g. technician).

    Methods:
        dispatch (predecision).
        form_valid (validation).
        form_invalid (validation).
        get (GET HTTP).
        post (POST HTTP).
    """
    model = User
    form_class = UserSoftRegisterForm
    success_url = reverse_lazy("home:main-home")
    template_name = None
    user_role = None
    authorized_roles: tuple[str, ...] = ()

    def dispatch(self, *args, **kwargs):
        """
        Ensures that the user who creating a new user
        has an appropriate role.
        """
        user = self.request.user
        is_allowed = (
            user.is_superuser
            or user.role in self.authorized_roles
        )

        # Redirects user only if user is neither
        # a superuser nor has an authorized role
        if not is_allowed:
            return redirect("home:main-home")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form: Form|ModelForm):
        """
        Form validation result.
        The messages should show if the form validated and create user successfully.

        Args:
            form (object): The User Soft Register Form that will be valid in case.
        """
        messages.success(
            request=self.request,
            message=_(f"کاربر با نقش {self.user_role} با موفقیت ساخته شد."),
            extra_tags="success"
        )

    def form_invalid(self, form: Form|ModelForm):
        """
        Form validation result if the validation failed.
        The message show  if the form will invalid and user had not yet.

        Args:
            form (object): The User Soft Register Form that will be invalid in some cases.
        """
        messages.error(
            request=self.request,
            message=_("مقادیر ارسالی درست نیست!"),
            extra_tags="danger"
        )

    def get(self, request):
        """
        Renderin the form class simply.
        """
        form = self.form_class()

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):
        """
        Validates the form data from the client,
        it the form is valid then create a new user
        with an appropriate role and showing the message,
        then redirect to the 'success-url'.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            result = register_or_continue_user(
                phone_number=cleaned_data['phone_number'],
                password=cleaned_data['password'],
                role=self.user_role
            )
            user = result['user']

            if result['action'] == 'already_exists':
                messages.error(
                    request=request,
                    message=_('این کاربر قبلا ثبت‌نام شده است')
                )
                return redirect('home:main-home')

            if result['action'] == 'complete_profile':
                request.session['user_role_registered_id'] = user.id
                if user.role == 'Vendor':
                    return redirect(
                        reverse_lazy(
                            f'external_partners:vendor-create'
                        )
                    )
                else:
                    return redirect(
                        reverse_lazy(
                            f'{self.user_role.lower()}s:{self.user_role.lower()}-create'
                        )
                    )

            # Keep created user-id in the session
            # to use it for creating a role object
            # base on created user-role
            request.session["user_role_registered_id"] = user.id
            request.session.modified = True

            self.form_valid(form=form)
            messages.success(
                request,
                _(f"کاربر با نقش {self.user_role} با موفقیت ساخته شد.")
            )

            return redirect(self.success_url)
        else:
            print(form.errors.as_json())

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )


class BaseUserProfileSoftUpdateView(LoginRequiredMixin, View):
    """
    Updating a user profile who created 'SOFT',
    updates its profile instantly after its created.

    Methods:
        dispatch (predecision).
        form_valid (validation).
        form_invalid (validation).
        get (GET HTTP).
        post (POST HTTP).
    """
    model = UserProfile
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy("home:main-home")
    template_name = None
    user = None
    authorized_roles: tuple[str, ...] = ()

    def dispatch(self, *args, **kwargs):
        """
        Ensures that the user who updating the user profile
        has an appropriate role.
        """
        user = self.request.user
        is_allowed = (
            user.is_superuser
            or user.role in self.authorized_roles
        )

        # Redirects user only if user is neither
        # a superuser nor has an authorized role
        if not is_allowed:
            return redirect("home:main-home")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form: Form|ModelForm):
        """
        Form validation result.
        The messages should show if the form validated and create user successfully.

        Args:
            form (object): The User Soft Register Form that will be valid in case.
        """
        messages.success(
            request=self.request,
            message=_(f"پروفایل کاربر با موفقیت ساخته شد."),
            extra_tags="success"
        )

    def form_invalid(self, form: Form|ModelForm):
        """
        Form validation result if the validation failed.
        The message show  if the form will invalid and user had not yet.

        Args:
            form (object): The User Soft Register Form that will be invalid in some cases.
        """
        messages.error(
            request=self.request,
            message=_("مقادیر ارسالی درست نیست!"),
            extra_tags="danger"
        )

    def get(self, request):
        """
        Renderin the form class simply.
        """
        form = self.form_class()

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

    def post(self, request):
        """
        Gets created user from the 'soft' approach
        by using sessions.
        Validates the form data from the client,
        if the form is valid then updates the user profile
        and redirect user to the 'success-url'.
        """
        form = self.form_class(request.POST)
        # Gets created user from the session
        user = request.session.get("user_role_registered_id")

        if form.is_valid():
            # Gets user profile
            profile = UserProfile.objects.get(user=user)

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            address = form.cleaned_data.get("address")
            # Updating the user's profile fields
            profile.first_name = first_name or None
            profile.last_name = last_name or None
            profile.address = address or None
            profile.save()

            self.form_valid(form=form)
            return redirect(self.success_url)
        else:
            self.form_invalid(form=form)

        context = {"form": form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
