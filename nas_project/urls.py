from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# --- 1. Users App Imports ---
from users.views import UserRegistrationViewSet, UserProfileViewSet, auth_client_view

# --- 2. Authentication Imports (Assuming Simple DRF Token Auth) ---
# If you created custom login/logout views, make sure they are imported:
from rest_framework.authtoken.views import obtain_auth_token 
# ^ This is the standard DRF view for token login

# --- 3. Other App Imports (Assume these ViewSets exist) ---
from items.views import ItemViewSet
from lending.views import LendingRequestViewSet
from messaging.views import MessageViewSet


# Initialize the router for API endpoints
router = DefaultRouter()

# ==================================================================
# API ROUTER REGISTRATION (Handles /api/{endpoint}/ and /api/{endpoint}/{pk}/)
# ==================================================================

# 1. Users App (Registration and Profile Management)
# Registration: Handles POST /api/users/ (for creating a new user)
router.register(r'users', UserRegistrationViewSet, basename='user-register')

# Profile: Handles GET, PUT, PATCH /api/profiles/me/
# Note: We'll use 'profiles' as the base, and map 'me' separately below
router.register(r'profiles', UserProfileViewSet, basename='user-profile')

# 2. Items App
router.register(r'items', ItemViewSet, basename='item')

# 3. Lending App
router.register(r'lending-requests', LendingRequestViewSet, basename='lending-request')

# 4. Messaging App
router.register(r'messages', MessageViewSet, basename='message')


# ==================================================================
# STANDARD DJANGO URL PATTERNS
# ==================================================================

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Simple HTML client for testing auth
    path('auth-client/', auth_client_view, name='auth-client'),

    # ------------------------------------------------------------------
    # API ENDPOINTS
    # ------------------------------------------------------------------

    # 1. API Router (Includes all registered viewsets: items, lending-requests, etc.)
    path('api/', include(router.urls)),

    # 2. Dedicated User Profile Endpoint (/api/me/)
    # We explicitly map the retrieve action to the base URL for the current user.
    # We use UserProfileViewSet which is set up to return request.user in get_object()
    path('api/me/', UserProfileViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'
    }), name='user-profile-me'),


    # 3. Token Authentication Endpoints (CRITICAL FOR LOGIN/LOGOUT)
    path('api/auth/token/login/', obtain_auth_token, name='token-login'), 
    # ^ Standard DRF login handler: expects username/password, returns token.

    # Logout (Token destruction) - Requires a custom view, often in users/views.py
    # path('api/auth/token/logout/', UserLogoutView.as_view(), name='token-logout'), 
    # ^ Uncomment this if you implement UserLogoutView

    # Fallback for browsable API login/logout links
    path('api/auth/', include('rest_framework.urls')), 
]
