from django.test import TestCase
from django.urls import reverse

from waterworks.apps.common.views.role_profile_create_view import User


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
