from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication endpoints (registration disabled)
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoints
    path('user/', views.get_current_user, name='current_user'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]
