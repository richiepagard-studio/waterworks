from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Represent a user in the system, including authentication and profile details.

	Attributes:
		phone_number (str): A unique identifier for authentication and send messages.
		username (str): A unique identifier for authentication, display name shown in the user interface.
		role (str): Choose what role user has to create another profile base on the role.

		is_active (bool): Activation status of user.
		is_admin (bool): True if the user is admin and false if it's just a rudimentary user.
		is_staff (bool): Just the validation of 'is_admin', True if the 'is_admin' be True.
	"""
	class UserRoleChoice(models.TextChoices):
		ADMIN = 'Admin', _('Admin')
		VENDOR = 'Vendor', _('Vendor')
		TECHNICIAN = 'Technician', _('Technician')
		CUSTOMER = 'Customer', _('Customer')
		EXPLORER = 'Explorer', _('Explorer')


	phone_number = PhoneNumberField(
		unique=True,
		region="IR",
		verbose_name=_("Phone Number"),
		help_text=_("Your original phone number to identify you and send messages.")
	)
	username = models.CharField(
		max_length=20,
		unique=True,
		null=True,
		blank=True,
		verbose_name=_("Username"),
		help_text=_("Display name shown in your profile interface, people will know you with this.")
	)
	role = models.CharField(
		max_length=20,
		choices=UserRoleChoice,
		default=UserRoleChoice.EXPLORER,
		verbose_name=_("Role"),
		help_text=_("User role that a profile will created base on the role.")
	)

	is_active = models.BooleanField(
		default=True,
		verbose_name=_("Active")
	)
	is_admin = models.BooleanField(
		default=False,
		verbose_name=_("Admin")
	)
	is_staff = models.BooleanField(
		default=False,
		verbose_name=_("Staff Status")
	)

	objects = UserManager()

	USERNAME_FIELD = "phone_number"

	class Meta:
		verbose_name = _("User")
		verbose_name_plural = _("Users")

	def __str__(self) -> str:
		activation_status = "active" if self.is_active else "not active"

		if self.username:
			return f"{self.phone_number} - {self.username} - {activation_status}"
		else:
			return f"{self.phone_number} - {activation_status}"
