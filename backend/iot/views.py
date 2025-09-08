from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response
from .models import GPSData
from .serializers import GPSDataSerializer
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
