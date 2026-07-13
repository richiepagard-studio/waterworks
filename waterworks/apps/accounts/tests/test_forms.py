from django.test import TestCase
from django.urls import reverse

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


class TestUserProfileUpdateView(TestCase):
	"""
	Test cases for testing user profile update view.
	"""
	
	def test_redirects_to_next_url_after_successful_update(self):
		"""
		Test that the view redirects to the next URL after a successful profile update.
		"""

		user = User.objects.create_user(
			phone_number='+989128762334',
			username='profiletestuser',
			password='&,iN3Bys'
		)
		url = reverse('accounts:user-profile-update', kwargs={'user_id': user.id})
		next_url = '/installations/1/'

		response = self.client.post(
			f'{url}?next={next_url}',
			data={
				'username': 'profiletestuser',
				'first_name': 'Test',
				'last_name': 'User',
				'address': 'Tehran',
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, next_url)
