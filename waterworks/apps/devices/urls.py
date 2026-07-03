from django.urls import path

from .views import (
	DeviceCreateView,
	DevicesListView,
	DeviceDetailView,
	DeviceUpdateView,
)


app_name = 'devices'

CRUD_URLS = [
	path('create/', DeviceCreateView.as_view(), name='device-create'),
	path('list/', DevicesListView.as_view(), name='devices-list'),
	path(
		'<int:device_pk>/<str:device_slug>/',
		DeviceDetailView.as_view(),
		name='device-detail'
	),
	path('update/<int:device_pk>/', DeviceUpdateView.as_view(), name='device-update'),
]
urlpatterns = CRUD_URLS
