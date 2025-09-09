from django.urls import path
from .views import GPSDataListCreateView, GPSDataDetailView, DeviceStatusLogListCreateView, DeviceStatusLogDetailView, relay_status, set_relay


urlpatterns = [
	path('gps/', GPSDataListCreateView.as_view(), name='gpsdata-list-create'),
	path('gps/<int:pk>/', GPSDataDetailView.as_view(), name='gpsdata-detail'),
	path('status-logs/', DeviceStatusLogListCreateView.as_view(), name='device-status-log-list-create'),
	path('status-logs/<int:pk>/', DeviceStatusLogDetailView.as_view(), name='device-status-log-detail'),

	#Device ON/OFF endpoints
	path("relay/<str:device_id>/", relay_status, name="relay_status"),
    path("relay/<str:device_id>/set/", set_relay, name="set_relay"),
]

