from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.external_partners.models import Vendor


class VendorRetrieveView(LoginRequiredMixin, View):
	"""
	Retrieving a vendor information,
	It must have showing the detail of a vendor.

	Methods:
		get (GET HTTP).
	"""
	template_name = "external_partners/vendor_pages/vendor_retrieve.html"

	def dispatch(self, request, *args, **kwargs):
		"""
		Ensures that the user who creating a new user
		has an appropriate role.
		"""
		user = request.user
		if user.is_authenticated:
			is_allowed = (
				user.is_superuser
				or user.role == 'Admin'
				or user.role == 'Vendor'
			)

			# Redirects user only if user is neither
			# a superuser nor has an authorized role
			if not is_allowed:
				return redirect('home:main-home')

		return super().dispatch(request, *args, **kwargs)

	def get(self, request, vendor_pk: int):
		"""
		Gets the vendor's PK and shows its detail.

		Args:
			vendor_pk (int): The primary-key of vendor.
		"""
		user = request.user
		role = user.role

		if role == 'Vendor':
			vendor = Vendor.objects.filter(user=user).first()
		elif role == 'Admin' or user.is_superuser:
			vendor = get_object_or_404(Vendor, pk=vendor_pk)

		context = {"vendor": vendor}
		return render(
			request=request,
            template_name=self.template_name,
            context=context
		)
