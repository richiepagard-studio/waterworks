from typing import TypedDict, Literal

from apps.accounts.models import User


class RegistrationResult(TypedDict):
    """
    Represents the result of a user registration attempt.
    """

    # The action taken during the registration process.
    action: Literal[
        'created',
        'already_exists',
        'complete_profile'
    ]
    user: User


def handle_existing_user(user: User, role: str) -> RegistrationResult:
    """
    Handle the case where an existing user is attempting to register
    with a specific role. Check if the user already has the requested role profile.
    If the user already has the role profile, return an action indicating that
    the profile already exists. Otherwise, return an action indicating that
    the user needs to complete their profile for the requested role.

    Arguments:
        user (User): The existing user object.
        role (str): The role for which the user is attempting to register.
    """

    profile_name = role.lower()

    # Check if the user already has the requested role profile
    if hasattr(user, profile_name):
        return {
            'action': 'already_exists',
            'user': user
        }

    # If the user does not have the requested role profile, return an action indicating
    # that the user needs to complete their profile for the requested role.
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
    Register a new user or continue with an existing user based on the provided
    phone number. If the user already exists, handle the existing user scenario.
    If the user does not exist, create a new user with the provided phone number,
    password, and role. The new user will be created with an inactive status.
    Return a dictionary containing the action taken and the user object.

    Arguments:
        phone_number (str): The phone number of the user attempting to register.
        password (str): The password for the new user.
        role (str): The role for which the user is attempting to register.
    """

    user = User.objects.filter(phone_number=phone_number).first()

    # If the user already exists, handle the existing user scenario
    if user:
        return handle_existing_user(
            user=user,
            role=role
        )

    # If the user does not exist, create a new user with the provided phone number,
    # password, and role. The new user will be created with an inactive status.
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
