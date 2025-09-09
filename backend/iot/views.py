from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import GPSData, DeviceStatusLog
from .serializers import GPSDataSerializer, DeviceStatusLogSerializer
from .authentication import DeviceTokenAuthentication


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
