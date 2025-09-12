from rest_framework import serializers
from .models import GPSData, DeviceStatusLog, Device
from django.db.models import Avg, Sum, Count, Q
from datetime import datetime, timedelta
import math


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


class StatisticsSerializer(serializers.Serializer):
	device_id = serializers.CharField()
	period = serializers.CharField()
	start_date = serializers.DateTimeField()
	end_date = serializers.DateTimeField()
	
	# Statistics data
	total_records = serializers.IntegerField()
	total_distance_km = serializers.FloatField()
	average_speed_kmh = serializers.FloatField()
	max_speed_kmh = serializers.FloatField()
	total_idle_time_hours = serializers.FloatField()
	total_moving_time_hours = serializers.FloatField()
	ignition_on_count = serializers.IntegerField()
	ignition_off_count = serializers.IntegerField()
	
	# Route data for mapping
	route_points = serializers.ListField(
		child=serializers.DictField()
	)


class DailyStatisticsSerializer(serializers.Serializer):
	date = serializers.DateField()
	total_distance_km = serializers.FloatField()
	average_speed_kmh = serializers.FloatField()
	max_speed_kmh = serializers.FloatField()
	total_idle_time_hours = serializers.FloatField()
	total_moving_time_hours = serializers.FloatField()
	route_points = serializers.ListField(
		child=serializers.DictField()
	)


class WeeklyStatisticsSerializer(serializers.Serializer):
	week_start = serializers.DateField()
	week_end = serializers.DateField()
	total_distance_km = serializers.FloatField()
	average_speed_kmh = serializers.FloatField()
	max_speed_kmh = serializers.FloatField()
	total_idle_time_hours = serializers.FloatField()
	total_moving_time_hours = serializers.FloatField()
	daily_breakdown = serializers.ListField(
		child=DailyStatisticsSerializer()
	)


class MonthlyStatisticsSerializer(serializers.Serializer):
	month = serializers.IntegerField()
	year = serializers.IntegerField()
	total_distance_km = serializers.FloatField()
	average_speed_kmh = serializers.FloatField()
	max_speed_kmh = serializers.FloatField()
	total_idle_time_hours = serializers.FloatField()
	total_moving_time_hours = serializers.FloatField()
	weekly_breakdown = serializers.ListField(
		child=WeeklyStatisticsSerializer()
	)


class YearlyStatisticsSerializer(serializers.Serializer):
	year = serializers.IntegerField()
	total_distance_km = serializers.FloatField()
	average_speed_kmh = serializers.FloatField()
	max_speed_kmh = serializers.FloatField()
	total_idle_time_hours = serializers.FloatField()
	total_moving_time_hours = serializers.FloatField()
	monthly_breakdown = serializers.ListField(
		child=MonthlyStatisticsSerializer()
	)
