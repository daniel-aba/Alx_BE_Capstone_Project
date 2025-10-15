from django.shortcuts import render 
from rest_framework import viewsets, permissions, mixins, status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

# Import the necessary components for JWT blacklisting (if implemented)
# We will use this in the UserLogoutView
# from rest_framework_simplejwt.tokens import RefreshToken

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

# -------------------------------------------------------------------------
# View for User Logout (POST /api/auth/token/logout/)
# This handles the server-side part of logging out by blacklisting tokens.
# -------------------------------------------------------------------------

class UserLogoutView(APIView):
    """
    Endpoint for user logout.
    The client is expected to send the Refresh Token in the request body.
    Requires authentication to ensure a user is logged in before attempting logout.
    """
    # User must be authenticated to access this view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # NOTE: This implementation requires 'rest_framework_simplejwt.token_blacklist'
        # to be added to INSTALLED_APPS in settings.py and migration run.
        
        # This part is currently commented out until you configure token blacklisting.
        """
        try:
            # Get the refresh token from the request data
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Blacklist the token, effectively logging the user out instantly
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            # Catch errors like missing token or invalid token
            return Response({"detail": "Invalid or missing refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        """
        
        # Simple success response if blacklisting is not configured, instructing client to discard tokens
        return Response({"detail": "Logout signal received. Client must discard tokens."}, 
                        status=status.HTTP_200_OK)
