from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy

from apps.common.models import BaseModel
from apps.accounts.models import User


class SkillLevelChoice(models.TextChoices):
	JUNIOR = "Junior", _("Junior")
	MIDLEVEL = "Midlevel", _("Midlevel")
	SENIOR = "Senior", _("Senior")


class Technician(BaseModel):
    """
    Model representing a technician with personal and contact information.

    Attributes:
        user (int, O2O): The user who is the Installation. This profile belongs to it.
        national_code (str): Technician national code for security info.
        installer_code (str): Generated code for the technician which is unique.
        experience_years (int, unsigned): How many years technician has experience.
        skill_level (str): Which skill level technician has.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    national_code = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(10)],
        verbose_name=_("National Code")
    )
    installer_code = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Installer Code")
    )
    experience_years = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Experience Years")
    )
    skill_level = models.CharField(
        max_length=9,
        choices=SkillLevelChoice.choices,
        null=True,
        blank=True,
        verbose_name=_("Skill Level")
    )

    class Meta:
        verbose_name = _("Technician")
        verbose_name_plural = _("Technicians")
        ordering = ['-created_at']

    def __str__(self) -> str:
        """
        Returns the user info by checking the important info.
        """
        lastname = self.user.userprofile.last_name or None
        username = self.user.username or None
        phone_number = self.user.phone_number

        if lastname and username:
            return f"{phone_number} - {username} - {lastname}"
        elif lastname and not username:
            return f"{phone_number} - {lastname}"
        elif username and not lastname:
            return f"{phone_number} - {username}"
        else:
            return f"{phone_number}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self.installer_code_generator()

        super().save(*args, **kwargs)

    def installer_code_generator(self) -> None:
        """
        Generates a unique code with length 6
        for a technician as a installer code.
        """
        length = 6
        generated_string = get_random_string(length)
        self.installer_code = generated_string

    @property
    def get_absolute_url(self):
        """
        Mostly use for retrieving a Installation.
        However, it returns a Installation detail but its PK.
        """
        return reverse_lazy(
            'technicians:technician-retrieve',
            kwargs={'technician_pk': self.pk}
        )
