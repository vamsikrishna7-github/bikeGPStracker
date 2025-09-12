from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import GPSData, DeviceStatusLog, Device
from .serializers import (
    GPSDataSerializer, DeviceStatusLogSerializer, DeviceSerializer,
    StatisticsSerializer, DailyStatisticsSerializer, WeeklyStatisticsSerializer,
    MonthlyStatisticsSerializer, YearlyStatisticsSerializer
)
from .authentication import DeviceTokenAuthentication
from rest_framework.decorators import api_view
from django.db.models import Avg, Sum, Count, Q, Max, Min
from datetime import datetime, timedelta, date
from django.utils import timezone
import math



class GPSDataListCreateView(mixins.ListModelMixin,
	mixins.CreateModelMixin,
	generics.GenericAPIView):
	queryset = GPSData.objects.all().order_by('-timestamp')
	serializer_class = GPSDataSerializer
	authentication_classes = [DeviceTokenAuthentication]
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GPSDataDetailView(mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	mixins.DestroyModelMixin,
	generics.GenericAPIView):
	queryset = GPSData.objects.all()
	serializer_class = GPSDataSerializer
	authentication_classes = [DeviceTokenAuthentication]
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class DeviceStatusLogListCreateView(mixins.ListModelMixin,
	mixins.CreateModelMixin,
	generics.GenericAPIView):
	queryset = DeviceStatusLog.objects.all().order_by('-created_at')
	serializer_class = DeviceStatusLogSerializer
	authentication_classes = [DeviceTokenAuthentication]
	permission_classes = [permissions.AllowAny]

	def get_queryset(self):
		qs = super().get_queryset()
		device_id = self.request.query_params.get('device_id')
		module = self.request.query_params.get('module')
		status_param = self.request.query_params.get('status')
		if device_id:
			qs = qs.filter(device_id=device_id)
		if module:
			qs = qs.filter(module=module)
		if status_param:
			qs = qs.filter(status=status_param)
		return qs

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeviceStatusLogDetailView(mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	generics.GenericAPIView):
	queryset = DeviceStatusLog.objects.all()
	serializer_class = DeviceStatusLogSerializer
	authentication_classes = [DeviceTokenAuthentication]
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

@api_view(["GET"])
def relay_status(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id)
        return Response(DeviceSerializer(device).data)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=404)

@api_view(["POST"])
def set_relay(request, device_id):
    try:
        device, _ = Device.objects.get_or_create(device_id=device_id)
        state = request.data.get("relay_state")
        if state is not None:
            device.relay_state = state
            device.save()
        return Response(DeviceSerializer(device).data)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


# Helper function to calculate distance between two GPS points
def calculate_distance(lat1, lon1, lat2, lon2):
	"""
	Calculate the great circle distance between two points on Earth in kilometers
	"""
	R = 6371  # Radius of the Earth in kilometers
	
	lat1_rad = math.radians(lat1)
	lon1_rad = math.radians(lon1)
	lat2_rad = math.radians(lat2)
	lon2_rad = math.radians(lon2)
	
	dlat = lat2_rad - lat1_rad
	dlon = lon2_rad - lon1_rad
	
	a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a))
	
	return R * c


def calculate_statistics(gps_data_queryset):
	"""
	Calculate statistics from GPS data queryset
	"""
	if not gps_data_queryset.exists():
		return {
			'total_records': 0,
			'total_distance_km': 0.0,
			'average_speed_kmh': 0.0,
			'max_speed_kmh': 0.0,
			'total_idle_time_hours': 0.0,
			'total_moving_time_hours': 0.0,
			'ignition_on_count': 0,
			'ignition_off_count': 0,
			'route_points': []
		}
	
	# Basic statistics
	total_records = gps_data_queryset.count()
	speeds = gps_data_queryset.values_list('speed', flat=True)
	ignition_statuses = gps_data_queryset.values_list('ignitionstatus', flat=True)
	
	# Calculate distance
	total_distance = 0.0
	route_points = []
	prev_point = None
	
	for point in gps_data_queryset.order_by('timestamp'):
		route_points.append({
			'latitude': float(point.latitude),
			'longitude': float(point.longitude),
			'timestamp': point.timestamp.isoformat(),
			'speed': float(point.speed),
			'ignition': point.ignitionstatus
		})
		
		if prev_point:
			distance = calculate_distance(
				prev_point.latitude, prev_point.longitude,
				point.latitude, point.longitude
			)
			total_distance += distance
		
		prev_point = point
	
	# Calculate time statistics
	first_record = gps_data_queryset.order_by('timestamp').first()
	last_record = gps_data_queryset.order_by('-timestamp').first()
	
	if first_record and last_record:
		total_time = (last_record.timestamp - first_record.timestamp).total_seconds() / 3600  # hours
		
		# Calculate idle time (when speed < 5 km/h or ignition is off)
		idle_records = gps_data_queryset.filter(
			Q(speed__lt=5) | Q(ignitionstatus=False)
		)
		idle_time = 0.0
		if idle_records.exists():
			idle_time = (idle_records.last().timestamp - idle_records.first().timestamp).total_seconds() / 3600
		
		moving_time = total_time - idle_time
	else:
		total_time = 0.0
		idle_time = 0.0
		moving_time = 0.0
	
	return {
		'total_records': total_records,
		'total_distance_km': round(total_distance, 2),
		'average_speed_kmh': round(sum(speeds) / len(speeds) if speeds else 0, 2),
		'max_speed_kmh': round(max(speeds) if speeds else 0, 2),
		'total_idle_time_hours': round(idle_time, 2),
		'total_moving_time_hours': round(moving_time, 2),
		'ignition_on_count': ignition_statuses.count(True),
		'ignition_off_count': ignition_statuses.count(False),
		'route_points': route_points
	}


@api_view(['GET'])
def device_statistics(request, device_id):
	"""
	Get statistics for a specific device
	Query parameters: period (day, week, month, year), start_date, end_date
	"""
	# Check authentication
	auth = DeviceTokenAuthentication()
	user, _ = auth.authenticate(request)
	if not user:
		return Response(
			{'error': 'Authentication required'}, 
			status=status.HTTP_401_UNAUTHORIZED
		)
	period = request.GET.get('period', 'day')
	start_date = request.GET.get('start_date')
	end_date = request.GET.get('end_date')
	
	# Get GPS data for the device
	queryset = GPSData.objects.filter(device_id=device_id)
	
	# Apply date filters
	if start_date:
		try:
			start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
			queryset = queryset.filter(timestamp__gte=start_dt)
		except ValueError:
			return Response(
				{'error': 'Invalid start_date format. Use ISO format.'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
	
	if end_date:
		try:
			end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
			queryset = queryset.filter(timestamp__lte=end_dt)
		except ValueError:
			return Response(
				{'error': 'Invalid end_date format. Use ISO format.'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
	
	# If no date filters, apply period-based filtering
	if not start_date and not end_date:
		now = timezone.now()
		if period == 'day':
			start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
			end_dt = now
		elif period == 'week':
			start_dt = now - timedelta(days=7)
			end_dt = now
		elif period == 'month':
			start_dt = now - timedelta(days=30)
			end_dt = now
		elif period == 'year':
			start_dt = now - timedelta(days=365)
			end_dt = now
		else:
			return Response(
				{'error': 'Invalid period. Use: day, week, month, or year'}, 
				status=status.HTTP_400_BAD_REQUEST
			)
		
		queryset = queryset.filter(timestamp__gte=start_dt, timestamp__lte=end_dt)
	
	# Calculate statistics
	stats = calculate_statistics(queryset)
	
	# Add metadata
	stats.update({
		'device_id': device_id,
		'period': period,
		'start_date': start_dt if 'start_dt' in locals() else None,
		'end_date': end_dt if 'end_dt' in locals() else None
	})
	
	serializer = StatisticsSerializer(stats)
	return Response(serializer.data)


@api_view(['GET'])
def daily_statistics(request, device_id):
	"""
	Get daily statistics for a device over a date range
	Query parameters: start_date, end_date
	"""
	# Check authentication
	auth = DeviceTokenAuthentication()
	user, _ = auth.authenticate(request)
	if not user:
		return Response(
			{'error': 'Authentication required'}, 
			status=status.HTTP_401_UNAUTHORIZED
		)
	start_date = request.GET.get('start_date')
	end_date = request.GET.get('end_date')
	
	if not start_date or not end_date:
		return Response(
			{'error': 'start_date and end_date are required'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	try:
		start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
		end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
	except ValueError:
		return Response(
			{'error': 'Invalid date format. Use ISO format.'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	daily_stats = []
	current_date = start_dt.date()
	end_date_obj = end_dt.date()
	
	while current_date <= end_date_obj:
		day_start = datetime.combine(current_date, datetime.min.time())
		day_end = datetime.combine(current_date, datetime.max.time())
		
		day_queryset = GPSData.objects.filter(
			device_id=device_id,
			timestamp__gte=day_start,
			timestamp__lte=day_end
		)
		
		stats = calculate_statistics(day_queryset)
		stats['date'] = current_date
		
		daily_stats.append(stats)
		current_date += timedelta(days=1)
	
	serializer = DailyStatisticsSerializer(daily_stats, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def weekly_statistics(request, device_id):
	"""
	Get weekly statistics for a device
	Query parameters: start_date, end_date
	"""
	# Check authentication
	auth = DeviceTokenAuthentication()
	user, _ = auth.authenticate(request)
	if not user:
		return Response(
			{'error': 'Authentication required'}, 
			status=status.HTTP_401_UNAUTHORIZED
		)
	start_date = request.GET.get('start_date')
	end_date = request.GET.get('end_date')
	
	if not start_date or not end_date:
		return Response(
			{'error': 'start_date and end_date are required'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	try:
		start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
		end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
	except ValueError:
		return Response(
			{'error': 'Invalid date format. Use ISO format.'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	weekly_stats = []
	current_date = start_dt.date()
	end_date_obj = end_dt.date()
	
	while current_date <= end_date_obj:
		# Get start of week (Monday)
		week_start = current_date - timedelta(days=current_date.weekday())
		week_end = week_start + timedelta(days=6)
		
		# Don't go beyond end_date
		if week_end > end_date_obj:
			week_end = end_date_obj
		
		week_start_dt = datetime.combine(week_start, datetime.min.time())
		week_end_dt = datetime.combine(week_end, datetime.max.time())
		
		week_queryset = GPSData.objects.filter(
			device_id=device_id,
			timestamp__gte=week_start_dt,
			timestamp__lte=week_end_dt
		)
		
		stats = calculate_statistics(week_queryset)
		stats.update({
			'week_start': week_start,
			'week_end': week_end
		})
		
		# Get daily breakdown for this week
		daily_breakdown = []
		day_date = week_start
		while day_date <= week_end:
			day_start = datetime.combine(day_date, datetime.min.time())
			day_end = datetime.combine(day_date, datetime.max.time())
			
			day_queryset = week_queryset.filter(
				timestamp__gte=day_start,
				timestamp__lte=day_end
			)
			
			day_stats = calculate_statistics(day_queryset)
			day_stats['date'] = day_date
			daily_breakdown.append(day_stats)
			
			day_date += timedelta(days=1)
		
		stats['daily_breakdown'] = daily_breakdown
		weekly_stats.append(stats)
		
		current_date = week_end + timedelta(days=1)
	
	serializer = WeeklyStatisticsSerializer(weekly_stats, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def monthly_statistics(request, device_id):
	"""
	Get monthly statistics for a device
	Query parameters: year
	"""
	# Check authentication
	auth = DeviceTokenAuthentication()
	user, _ = auth.authenticate(request)
	if not user:
		return Response(
			{'error': 'Authentication required'}, 
			status=status.HTTP_401_UNAUTHORIZED
		)
	year = request.GET.get('year', datetime.now().year)
	
	try:
		year = int(year)
	except ValueError:
		return Response(
			{'error': 'Invalid year format'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	monthly_stats = []
	
	for month in range(1, 13):
		month_start = datetime(year, month, 1)
		if month == 12:
			month_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
		else:
			month_end = datetime(year, month + 1, 1) - timedelta(seconds=1)
		
		month_queryset = GPSData.objects.filter(
			device_id=device_id,
			timestamp__gte=month_start,
			timestamp__lte=month_end
		)
		
		stats = calculate_statistics(month_queryset)
		stats.update({
			'month': month,
			'year': year
		})
		
		# Get weekly breakdown for this month
		weekly_breakdown = []
		current_date = month_start.date()
		month_end_date = month_end.date()
		
		while current_date <= month_end_date:
			week_start = current_date - timedelta(days=current_date.weekday())
			week_end = week_start + timedelta(days=6)
			
			if week_end > month_end_date:
				week_end = month_end_date
			
			week_start_dt = datetime.combine(week_start, datetime.min.time())
			week_end_dt = datetime.combine(week_end, datetime.max.time())
			
			week_queryset = month_queryset.filter(
				timestamp__gte=week_start_dt,
				timestamp__lte=week_end_dt
			)
			
			week_stats = calculate_statistics(week_queryset)
			week_stats.update({
				'week_start': week_start,
				'week_end': week_end
			})
			
			weekly_breakdown.append(week_stats)
			current_date = week_end + timedelta(days=1)
		
		stats['weekly_breakdown'] = weekly_breakdown
		monthly_stats.append(stats)
	
	serializer = MonthlyStatisticsSerializer(monthly_stats, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def yearly_statistics(request, device_id):
	"""
	Get yearly statistics for a device
	Query parameters: start_year, end_year
	"""
	# Check authentication
	auth = DeviceTokenAuthentication()
	user, _ = auth.authenticate(request)
	if not user:
		return Response(
			{'error': 'Authentication required'}, 
			status=status.HTTP_401_UNAUTHORIZED
		)
	start_year = request.GET.get('start_year', datetime.now().year - 1)
	end_year = request.GET.get('end_year', datetime.now().year)
	
	try:
		start_year = int(start_year)
		end_year = int(end_year)
	except ValueError:
		return Response(
			{'error': 'Invalid year format'}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	yearly_stats = []
	
	for year in range(start_year, end_year + 1):
		year_start = datetime(year, 1, 1)
		year_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
		
		year_queryset = GPSData.objects.filter(
			device_id=device_id,
			timestamp__gte=year_start,
			timestamp__lte=year_end
		)
		
		stats = calculate_statistics(year_queryset)
		stats['year'] = year
		
		# Get monthly breakdown for this year
		monthly_breakdown = []
		for month in range(1, 13):
			month_start = datetime(year, month, 1)
			if month == 12:
				month_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
			else:
				month_end = datetime(year, month + 1, 1) - timedelta(seconds=1)
			
			month_queryset = year_queryset.filter(
				timestamp__gte=month_start,
				timestamp__lte=month_end
			)
			
			month_stats = calculate_statistics(month_queryset)
			month_stats.update({
				'month': month,
				'year': year
			})
			
			monthly_breakdown.append(month_stats)
		
		stats['monthly_breakdown'] = monthly_breakdown
		yearly_stats.append(stats)
	
	serializer = YearlyStatisticsSerializer(yearly_stats, many=True)
	return Response(serializer.data)
