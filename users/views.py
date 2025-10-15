from django.shortcuts import render 
from rest_framework import viewsets, permissions, mixins # Standard imports for the ViewSets
from django.contrib.auth import get_user_model

from .serializers import UserSerializer # Import the comprehensive UserSerializer

User = get_user_model()

# --- New View for Frontend Client (Kept for continuity) ---
def auth_client_view(request):
    """
    Renders the HTML template containing the frontend authentication client.
    This template must be placed at users/templates/users/auth_client.html.
    """
    return render(request, 'users/auth_client.html')
# --- End of New View ---

# -------------------------------------------------------------------------
# ViewSet for User Registration (POST /api/users/)
# This replaces the old UserRegistrationView and UserViewSet's POST logic.
# -------------------------------------------------------------------------

class UserRegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint for user registration. 
    Handles POST requests to create a new user account using the UserSerializer.
    CRITICAL: permissions.AllowAny allows unauthenticated users to register.
    """
    serializer_class = UserSerializer
    # This is a public endpoint, so we allow any user to access it.
    permission_classes = [permissions.AllowAny]


# -------------------------------------------------------------------------
# ViewSet for User Profile Management (GET/PUT/PATCH /api/users/me/ or similar)
# This replaces the profile management aspects of the old UserViewSet.
# -------------------------------------------------------------------------

class UserProfileViewSet(mixins.RetrieveModelMixin, 
                         mixins.UpdateModelMixin, 
                         viewsets.GenericViewSet):
    """
    Endpoint for viewing and updating the currently authenticated user's profile.
    Requires authentication.
    """
    # Setting queryset is still good practice, though get_object overrides it for safety.
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    # Requires authentication for all profile actions
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        """
        Overrides the standard get_object to return the profile of the 
        currently authenticated user, ensuring a user can only edit themselves.
        """
        # Ensure a user can only retrieve/update their own profile
        return self.request.user
