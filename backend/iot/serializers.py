from rest_framework import serializers
from .models import GPSData, DeviceStatusLog, Device


class GPSDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = GPSData
		fields = [
			'id',
			'device_id',
			'latitude',
			'longitude',
			'altitude',
			'course',
			'speed',
			'ignitionstatus',
			'timestamp',
		]
		read_only_fields = ['id', 'timestamp']


class DeviceStatusLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeviceStatusLog
		fields = [
			'id',
			'device_id',
			'module',
			'status',
			'message',
			'code',
			'created_at',
		]
		read_only_fields = ['id', 'created_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["device_id", "relay_state"]
