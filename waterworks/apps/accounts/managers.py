from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
	"""
    Custom base user manager to manage users creation such as create superuser.

    Methods:
        create_user: Create a rudimentary user with required fields.
        create_superuser: Create a superuser to set full access on admin panel with required fields.
    """
	def create_user(self, phone_number: str, role: str='Explorer', username: str=None, password=None):
		"""
        Create a rudimentary user with required fields,
        Check if user has phone number and username to verify them.

        Arguments:
            phone_number (str): User phone number, user will verify by it.
            username (str): A unique identifier for authentication, display name shown in the user interface.
            password (str): Could be None because user could register with OTP code.
        """
		if not phone_number:
			raise ValueError(_('User must has a phone number to identify.'))

		user = self.model(
			phone_number=phone_number,
			role=role,
			username=username
		)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, phone_number: str, role: str='Admin', username: str=None, password=None):
		"""
        Create a superuser with reuired fields and activation status of Is Superuser.
        Check if the Is Staff and Is Superuser status are active for created superuser.

        Arguments:
            phone_number (str): User phone number, user will verify by it.
            username (str): A unique identifier for authentication, display name shown in the user interface.
            password (str): Could be None because user could register with OTP code or by 'createsuperuser' command.
        """
		user = self.create_user(
			phone_number=phone_number,
			role=role,
			username=username,
			password=password
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		return user
