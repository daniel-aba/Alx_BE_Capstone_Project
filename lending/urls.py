from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LendingRequestViewSet

router = DefaultRouter()
router.register(r'lending-requests', LendingRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]