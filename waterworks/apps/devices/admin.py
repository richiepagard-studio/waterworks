from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'model',
		'installed_count',
		'guarantee',
		'stock_quantity',
		'is_in_stock'
	)
	list_filter = ('is_active', 'is_in_stock', 'created_at', 'updated_at')
	search_fields = ('name', 'model')
	prepopulated_fields = {'slug': ('name', 'model')}
