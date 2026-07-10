from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from apps.common.models import BaseModel
from apps.common.utils import path_with_hash
from .managers import InStockDevicesManager


def banner_path(instance, filename: str) -> str:
	"""
	Uploads the device banner/image file with a hash
	method to encrypting the file.
	"""
	return f"devices/{path_with_hash(filename)}"


class Device(BaseModel):
	"""
	Represents to the devices that Linux Project provide.

	Attributes:
		name (str): The original name of the device.		
		model (str): The model of the device.
		installed_count (int, unsigned): Installation count of the device.
		guarantee (int): The months device guaranteed.
		stock_quantity (int): The stock, invenroty of the device.
		is_in_stock (bool): The availability status of device.
		image (str, file): Device's banner, encrypting with path-to-hash method.
		slug (str): Device slug wich filled by name and model of device.
	"""
	name = models.CharField(
		max_length=50,
		verbose_name=_('Name')
	)
	model = models.CharField(
		max_length=50,
		verbose_name=_('Model')
	)
	installed_count = models.PositiveIntegerField(
		default=0,
		verbose_name=_('Installed Count')
	)
	guarantee = models.PositiveIntegerField(
		null=True,
		blank=True,
		verbose_name=_('Guarantee'),
		help_text=_('ماه وارد کنید (مثال: ۲۴)')
	)
	stock_quantity = models.PositiveIntegerField(
		null=True,
		blank=True,
		verbose_name=_('Stock Quantity'),
		help_text=_('تعداد موجودی (برای سایت)')
	)
	is_in_stock = models.BooleanField(
		default=True,
		verbose_name=_('In Stock'),
		help_text=_('وضعیت موجودی در سایت.')
	)
	description = models.TextField(
		null=True,
		blank=True,
		verbose_name=_('Description')
	)
	image = models.ImageField(
		upload_to=banner_path,
		blank=True
	)
	slug = models.SlugField(
        unique=True,
        verbose_name=_('Slug'),
        null=True,
        blank=True,
        allow_unicode=True
    )

	objects = models.Manager()
	availables = InStockDevicesManager()	

	class Meta:
		verbose_name = _('Device')
		verbose_name_plural = _('Devices')
		ordering = ['-created_at']

	def __str__(self) -> str:
		return f"{self.name} - {self.model}"

	@classmethod
	def most_installation(cls, length: int):
		"""
		Returning the most installed devices
		which referes to the most popular devices
		based on the 'installed-count' of each device.

		Arguments:
			length (int): The number of returning objects.
		"""
		devices = cls.objects.filter(
			is_active=True).order_by('-installed_count')[:length]

		return devices

	@classmethod
	def last_devices(cls, length: int):
		"""
		Returning the last added devices in database.
		It refers to the newest 'created-at' devices.

		Arguments:
			length (int): The number of returning objects.
		"""
		devices = cls.availables.filter(is_active=True).order_by('-created_at')[:length]

		return devices

	def get_absolute_url(self):
		"""
		Returning back a device retrieve/detail URL.
		Uses the reverse-lazy URL method and gets the device
		by its PK and Slug.
		"""
		return reverse_lazy(
			'devices:device-detail',
			kwargs={'device_pk': self.pk, 'device_slug': self.slug}
		)
