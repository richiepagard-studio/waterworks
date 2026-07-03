from django.db import transaction

from .models import Device


@transaction.atomic
def update_device(*, device: Device, data: dict) -> Device:
    """
    Updates a device with validated data.

    Arguments:
        device (obj): The device object will updated.
        data (dict): The incoming data from the form, cleaned-data.
    """

    for field, value in data.items():
        setattr(device, field, value)

    # Business rule
    device.is_in_stock = device.stock_quantity > 0

    device.save()

    return device
