# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    UserRegistrationView, 
    UserLoginView, 
    UserLogoutView
)

# Router for the User Profile Management (CRUD, requires authentication)
router = DefaultRouter()
# Maps to /api/users/ and /api/users/{id}/
# The base name is 'user'
router.register(r'', UserViewSet, basename='user') 

urlpatterns = [
    # 1. Custom Paths for Authentication (AllowAny)
    # Maps to: POST /api/users/register/
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # Maps to: POST /api/users/login/
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # Maps to: POST /api/users/logout/ (Requires IsAuthenticated)
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    # 2. ViewSet Paths (Profile Management)
    # Includes paths like GET/PUT/DELETE /api/users/{id}/ 
    # and potentially GET /api/users/ for staff (depending on permissions in UserViewSet)
    path('', include(router.urls)),
]