import logging
from colorama import Fore, Style, init

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.accounts.models import UserProfile


# Configure logging for the accounts signal module
logger = logging.getLogger(__name__)
init(autoreset=True)


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creating user-profile suddenly after
    user object registered/created.
    """
    if created:
        UserProfile.objects.create(user=instance)

        logger.debug(
            f'User profile created for user: {Fore.LIGHTGREEN_EX}{instance.username}{Style.RESET_ALL}'
        )


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the created user-profile instantly after it created.
    """

    # Save the created instance
    instance.userprofile.save()
    logger.debug(
        f'User profile saved for user: {Fore.LIGHTBLUE_EX}{instance.username}{Style.RESET_ALL}'
    )
