from django.db import models


class GPSData(models.Model):
	device_id = models.CharField(max_length=100)
	latitude = models.FloatField()
	longitude = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.device_id} @ ({self.latitude}, {self.longitude}) at {self.timestamp}"
