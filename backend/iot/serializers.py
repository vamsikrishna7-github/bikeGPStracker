from rest_framework import serializers
from .models import GPSData


class GPSDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = GPSData
		fields = [
			'id',
			'device_id',
			'latitude',
			'longitude',
			'timestamp',
		]
		read_only_fields = ['id', 'timestamp']

