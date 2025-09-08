from typing import Optional, Tuple
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class DevicePrincipal:
	is_authenticated = True

	def __init__(self, device_id: str) -> None:
		self.device_id = device_id
		self.username = f"device:{device_id}"

	def __str__(self) -> str:
		return self.username


class DeviceTokenAuthentication(BaseAuthentication):
	"""
	Authenticate using a device token sent as a Bearer token.
	Token value must match one of settings.IOT_DEVICE_IDS. No expiry.
	"""

	keyword = b'bearer'

	def authenticate(self, request) -> Optional[Tuple[DevicePrincipal, None]]:
		auth_header = get_authorization_header(request).split()
		if not auth_header:
			return None

		if auth_header[0].lower() != self.keyword:
			return None

		if len(auth_header) == 1:
			raise AuthenticationFailed('Invalid Authorization header. No credentials provided.')
		if len(auth_header) > 2:
			raise AuthenticationFailed('Invalid Authorization header. Token string should not contain spaces.')

		try:
			device_token = auth_header[1].decode()
		except Exception:
			raise AuthenticationFailed('Invalid Authorization header. Token is not valid UTF-8.')

		allowed_ids = getattr(settings, 'IOT_DEVICE_IDS', [])
		if device_token in allowed_ids:
			return DevicePrincipal(device_token), None

		return None

