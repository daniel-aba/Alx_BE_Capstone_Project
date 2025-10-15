from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import ViewSets and utility view from the users app
from users.views import UserRegistrationViewSet, UserProfileViewSet, auth_client_view
# You will need to import your login and logout views if they are custom:
# from users.views import UserLoginView, UserLogoutView 
# (Assuming your login/logout views are handled by the standard token auth included below)


# Initialize the router for API endpoints
router = DefaultRouter()

# ------------------------------------------------------------------
# 1. User Registration (Handles POST /api/users/)
# This maps the POST request to the CreateModelMixin in UserRegistrationViewSet.
# ------------------------------------------------------------------
router.register(r'users', UserRegistrationViewSet, basename='user-register')

# ------------------------------------------------------------------
# 2. Other App ViewSets (You will need to add these later)
# Example:
# from items.views import ItemViewSet
# router.register(r'items', ItemViewSet, basename='item')
# ------------------------------------------------------------------


# Standard Django URL Patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Simple HTML client for testing auth
    path('auth-client/', auth_client_view, name='auth-client'),

    # ------------------------------------------------------------------
    # API Endpoints
    # ------------------------------------------------------------------

    # 1. API Router (Includes /api/users/, and any future registered viewsets)
    path('api/', include(router.urls)),

    # 2. Custom Profile Retrieval Endpoint (/api/me/)
    # This maps the detail actions (GET, PUT, PATCH) of UserProfileViewSet 
    # to the endpoint /api/me/ for the currently authenticated user.
    path('api/me/', UserProfileViewSet.as_view({
        'get': 'retrieve', 
        'put': 'update', 
        'patch': 'partial_update'
    }), name='user-profile-me'),

    # 3. Token Authentication Endpoints 
    # This assumes you are using drf-authtoken or a similar custom solution 
    # that registers its URLs separately. 
    path('api/auth/', include('rest_framework.urls')), # For browsable API login/logout
    
    # If you have custom login/logout views, uncomment and map them:
    # path('api/auth/token/login/', UserLoginView.as_view(), name='login'),
    # path('api/auth/token/logout/', UserLogoutView.as_view(), name='logout'),
]
