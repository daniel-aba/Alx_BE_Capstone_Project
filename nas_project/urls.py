# nas_project/urls.py 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/items/', include('items.urls')),
    path('api/lending/', include('lending.urls')),  # Add this line
    
    # DRF login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]