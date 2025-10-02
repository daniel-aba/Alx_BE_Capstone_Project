# nas_project/urls.py 
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from items.views import ItemViewSet, AvailabilityViewSet

# Use DRF's DefaultRouter to automatically generate URL patterns for ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include(router.urls)),

    # DRF login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]