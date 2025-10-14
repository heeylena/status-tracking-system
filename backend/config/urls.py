"""
URL configuration for Employee Status Tracking System.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from employees.auth_views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Employee and status endpoints
    path('api/', include('employees.urls')),
]

# Customize admin site
admin.site.site_header = "Employee Status Tracking System"
admin.site.site_title = "Employee Status Admin"
admin.site.index_title = "Administration Dashboard"
