from django.shortcuts import render 
from rest_framework import viewsets, generics, permissions # Import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer
from rest_framework.status import HTTP_200_OK

User = get_user_model()

# --- New View for Frontend Client ---
def auth_client_view(request):
    """
    Renders the HTML template containing the frontend authentication client.
    This template must be placed at users/templates/users/auth_client.html.
    """
    return render(request, 'users/auth_client.html')
# --- End of New View ---

# --- User Profile/Management (Conditional Permissions) ---
class UserViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD functionality for the User model (for staff or authorized users).
    Allows creation (POST) by anyone, but restricts all other methods.
    """
    queryset = User.objects.all().order_by('id') 
    serializer_class = UserSerializer
    
    # 💥 UPDATED: Removed static permission_classes and implemented get_permissions
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Allow POST (Create) without authentication
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        
        # Require authentication for all other actions (GET, PUT, PATCH, DELETE)
        return [permissions.IsAuthenticated()]

# --- Registration View (Allows Any) ---
class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration (creating a new user account).
    Returns user data along with the generated auth token.
    (This is the primary registration endpoint, using AllowAny.)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 

    # Overriding create to return the user data and token correctly after creation
    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        # Add the token and user ID to the instance for response
        serializer.instance.token = token.key
        serializer.instance.user_id = user.pk

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Extract the serialized user object which now contains token and user_id
        if response.status_code == 201:
            return Response({
                'token': response.data.pop('token'),
                'user_id': response.data.pop('user_id'),
                'username': response.data['username'],
                'email': response.data['email'],
                # You can choose what other fields to return here
            }, status=HTTP_200_OK)
        return response


# --- New Login View (Allows Any) ---
class UserLoginView(ObtainAuthToken):
    """
    API View to handle user login.
    Accepts username and password, returns an auth token and user details.
    """
    def post(self, request, *args, **kwargs):
        # Use DRF's built-in AuthTokenSerializer logic for validation
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the token and user details
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
        })

# --- New Logout View (Requires Authentication) ---
class UserLogoutView(APIView):
    """
    API View to handle user logout by deleting the auth token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's current token
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=HTTP_200_OK)
        except Exception:
            # Token might already be deleted or not exist, still treat as success
            return Response({"detail": "Successfully logged out."}, status=HTTP_200_OK)
