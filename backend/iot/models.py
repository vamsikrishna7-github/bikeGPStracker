from django.db import models


class GPSData(models.Model):
	device_id = models.CharField(max_length=100)
	latitude = models.FloatField()
	longitude = models.FloatField()
	altitude = models.FloatField(default=0.0)  # meters
	course = models.FloatField(default=0.0)  # degrees 0-359
	speed = models.FloatField(default=0.0)  # km/h
	ignitionstatus = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.device_id} @ ({self.latitude}, {self.longitude}) at {self.timestamp}"


class DeviceStatusLog(models.Model):
	MODULE_CHOICES = [
		('NODEMCU', 'NodeMCU'),
		('NEO6M', 'NEO-6M'),
		('SIM800L', 'SIM800L'),
		('WIFI', 'WiFi'),
	]

	STATUS_CHOICES = [
		('WAITING_GPS', 'Waiting for GPS location'),
		('GPS_LOST', 'GPS lost'),
		('LOW_BATTERY', 'Low battery'),
		('NETWORK_ISSUE', 'Network issue'),
		('INFO', 'Info'),
		('WARNING', 'Warning'),
		('ERROR', 'Error'),
	]

	device_id = models.CharField(max_length=100)
	module = models.CharField(max_length=20, choices=MODULE_CHOICES)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INFO')
	message = models.TextField(blank=True, default='')
	code = models.CharField(max_length=50, blank=True, default='')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.device_id} [{self.module}] {self.status} - {self.created_at}"
