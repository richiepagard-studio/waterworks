from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.technicians.models import Technician


class TechnicianRetrieveView(LoginRequiredMixin, View):
	"""
	Retrieving a technician information,
	It must have showing the detail of a technician(installer).

	Methods:
		get (GET HTTP).
	"""
	template_name = "technicians/technician_retrieve.html"

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
				or user.role == 'Technician'
			)

			# Redirects user only if user is neither
			# a superuser nor has an authorized role
			if not is_allowed:
				return redirect('accounts:user-dashboard')

		return super().dispatch(request, *args, **kwargs)

	def get(self, request, technician_pk: int):
		"""
		Gets the technician's PK and shows its detail.

		Args:
			technician_pk (int): The primary-key of technician.
		"""
		user = request.user
		role = user.role

		if role == 'Technician':
			technician = Technician.objects.prefetch_related('installations').get(user=user)
			last_installations = technician.installations.all()
			installations_count = len(last_installations)
		elif role == 'Admin' or user.is_superuser:
			technician = get_object_or_404(Technician, pk=technician_pk)
			last_installations = technician.installations.all()
			installations_count = len(last_installations)

		context = {
			"technician": technician,
			"last_installations": last_installations[:5],
			"installations_count": installations_count
		}
		return render(
			request=request,
            template_name=self.template_name,
            context=context
		)
