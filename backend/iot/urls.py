from django.urls import path
from .views import (
	GPSDataListCreateView, GPSDataDetailView, 
	DeviceStatusLogListCreateView, DeviceStatusLogDetailView, 
	relay_status, set_relay,
	device_statistics, daily_statistics, weekly_statistics,
	monthly_statistics, yearly_statistics
)


urlpatterns = [
	path('gps/', GPSDataListCreateView.as_view(), name='gpsdata-list-create'),
	path('gps/<int:pk>/', GPSDataDetailView.as_view(), name='gpsdata-detail'),
	path('status-logs/', DeviceStatusLogListCreateView.as_view(), name='device-status-log-list-create'),
	path('status-logs/<int:pk>/', DeviceStatusLogDetailView.as_view(), name='device-status-log-detail'),

	#Device ON/OFF endpoints
	path("relay/<str:device_id>/", relay_status, name="relay_status"),
    path("relay/<str:device_id>/set/", set_relay, name="set_relay"),
    
    # Statistics endpoints
    path("statistics/<str:device_id>/", device_statistics, name="device-statistics"),
    path("statistics/<str:device_id>/daily/", daily_statistics, name="daily-statistics"),
    path("statistics/<str:device_id>/weekly/", weekly_statistics, name="weekly-statistics"),
    path("statistics/<str:device_id>/monthly/", monthly_statistics, name="monthly-statistics"),
    path("statistics/<str:device_id>/yearly/", yearly_statistics, name="yearly-statistics"),
]

