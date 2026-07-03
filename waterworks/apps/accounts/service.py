from typing import TypedDict, Literal

from apps.accounts.models import User



class RegistrationResult(TypedDict):
    action: Literal[
        'created',
        'already_exists',
        'complete_profile'
    ]
    user: User


def handle_existing_user(user: User, role: str) -> RegistrationResult:
    """
    Handle an already existing user.
    """

    profile_name = role.lower()

    if hasattr(user, profile_name):
        return {
            'action': 'already_exists',
            'user': user
        }

    return {
        'action': 'complete_profile',
        'user': user
    }


def register_or_continue_user(
    phone_number: str,
    password: str,
    role: str
) -> RegistrationResult:
    """
    Create a new user or continute registeration
    for an existing user.

    Check whether an existing user already has the requested role profile.
    """

    user = User.objects.filter(phone_number=phone_number).first()

    if user:
        return handle_existing_user(
            user=user,
            role=role
        )

    user = User.objects.create_user(
        phone_number=phone_number,
        password=password,
        role=role
    )

    user.is_active = False
    user.save()

    return {
        'action': 'created',
        'user': user
    }
