from django.test import TestCase

from apps.accounts.models import User
from apps.accounts.forms import UserRegisterForm


class TestRegisterForm(TestCase):
	"""
	Test cases for testing user registration form.
	The user who created with this form is going to have
	'Explorer' role.

	TestCases Methods:
		test_valid_data;
		test_empty_data;
		test_unmatched_passwords;
	"""

	def test_valid_data(self):
		"""
		Test the for sending valid data to the form.
		"""

		form = UserRegisterForm(
			data = {
				'phone_number': '+989128762332',
				'password': '&,iN3Bys',
				'password_repeat': '&,iN3Bys'
			}
		)

		self.assertTrue(form.is_valid())

	def test_empty_data(self):
		"""
		Tests if the sent data is empty(None) from the client.
		Checks the validated status of form if the sent data is empty,
		also, checks if the length of errors are about to
		the number of required fields.
		"""

		form = UserRegisterForm(
			data = {}
		)

		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 3)

	def test_unmatched_passwords(self):
		"""
		Checks if the entered passwords are unmatched.
		The 'password' and 'password_repeat' fields
		has to be matched together.
		"""

		form = UserRegisterForm(
			data = {
				'phone_number': '+989126546996',
				'password': '&,iN3Bys',
				'password_repeat': '&,iN3Bys??'
			}
		)

		self.assertEqual(len(form.errors), 1)
		self.assertTrue(form.has_error)

