from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.accounts.models import User
from apps.common.utils import path_with_hash



def avatar_path(instance, filename: str) -> str:
    """
    Uploads the user profile image file with a hash
    method to encrypting the file.
    """
    return f"userprofile/avatar/{path_with_hash(filename)}"


class UserProfile(BaseModel):
    """
    Represents to the Users Profiles.
    Basic information of users with different roles.

    Attributes:
        user (int, O2O): The user who is the owner of this profile.
        first_name (str): Provides user's first-name.
        last_name (str): Provides user's last name.
        address (str): Provides user's home address.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        help_text=_('User who is the owner of this profile.')
    )
    first_name = models.CharField(
        max_length=30,
        db_index=True,
        null=True,
        blank=True,
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        max_length=30,
        db_index=True,
        null=True,
        blank=True,
        verbose_name=_('Last name')
    )
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Address')
    )
    avatar_image = models.ImageField(
        upload_to=avatar_path,
        blank=True,
        verbose_name=_('Avatar Image')
    )

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('Users Profiles')

    def __str__(self) -> str:
        return f"{self.user}"

    @property
    def fullname(self) -> str:
        """
        Fullname of a user which contains first-name
        and last-name together.
        """
        first_name = self.first_name or None
        last_name = self.last_name or None
        fullname = None

        if first_name and last_name:
            fullname = first_name + " " + last_name
        elif first_name and not last_name:
            fullname = first_name
        elif not first_name and last_name:
            fullname = last_name
        else:
            fullname = None

        return fullname
