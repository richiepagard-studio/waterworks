from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

from .models import Installation
from apps.devices.models import Device


@receiver(post_save, sender=Installation)
def update_device_installed_count(sender, instance, created, **kwargs):
    """
    Signal for updating the device installed-count 
    and stock-quantity that created installation with.

    sender (obj): The model class.
    instance (obj): The actual instance being saved.
    created (bool): True if a new record was created.
    """
    if created:
        # Updating the device installed count and save it
        Device.objects.filter(pk=instance.device_id).update(
            # Preventing the race condition
            installed_count = F('installed_count') + 1,
            stock_quantity = F('stock_quantity') - 1
        )
