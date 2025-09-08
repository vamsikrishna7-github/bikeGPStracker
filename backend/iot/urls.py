from django.urls import path
from .views import GPSDataListCreateView, GPSDataDetailView


urlpatterns = [
	path('gps/', GPSDataListCreateView.as_view(), name='gpsdata-list-create'),
	path('gps/<int:pk>/', GPSDataDetailView.as_view(), name='gpsdata-detail'),
]

