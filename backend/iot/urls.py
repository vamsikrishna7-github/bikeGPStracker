from django.urls import path
from .views import GPSDataListCreateView, GPSDataDetailView, DeviceStatusLogListCreateView, DeviceStatusLogDetailView


urlpatterns = [
	path('gps/', GPSDataListCreateView.as_view(), name='gpsdata-list-create'),
	path('gps/<int:pk>/', GPSDataDetailView.as_view(), name='gpsdata-detail'),
	path('status-logs/', DeviceStatusLogListCreateView.as_view(), name='device-status-log-list-create'),
	path('status-logs/<int:pk>/', DeviceStatusLogDetailView.as_view(), name='device-status-log-detail'),
]

