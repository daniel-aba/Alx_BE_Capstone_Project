from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, AvailabilityViewSet

router = DefaultRouter()
router.register(r'', ItemViewSet)
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]