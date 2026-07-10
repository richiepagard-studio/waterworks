from django.db import models


class InStockDevicesManager(models.Manager):
    """
    Manager to filter all the devices
    those are available.
    """
    def get_queryset(self):
        from apps.devices.models import Device

        return super().get_queryset().filter(is_in_stock=True)
