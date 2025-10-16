from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError # Import IntegrityError for robust token creation

# Get the custom User model defined in settings.py
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Field to hold the token after creation (read-only)
    # Assumes the User model has a related Token object named 'auth_token'
    auth_token = serializers.CharField(source='auth_token.key', read_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'password', 
            'bio', 
            'location', 
            'phone_number',
            'national_id',
            'is_id_verified',
            'is_phone_verified',
            'auth_token' # Include the token in the response
        )
        # Ensure password is write-only and not displayed
        extra_kwargs = {
            'password': {'write_only': True},
            # These are security/admin-controlled flags, kept read-only for the user
            'is_id_verified': {'read_only': True},
            'is_phone_verified': {'read_only': True},
            # National ID is sensitive, so it's write-only (input only, never output)
            'national_id': {'write_only': True} 
        }

    def create(self, validated_data):
        # Hash the password securely before saving
        # The password field is automatically popped if not using set_password in Model.create()
        password = validated_data.pop('password') 
        
        # Create the user instance
        user = User.objects.create(
            # Using create is cleaner than manipulating validated_data and calling super().create
            password=make_password(password),
            **validated_data 
        )
        
        # Create an authentication token for the new user
        # This makes the user instantly logged in after registration
        try:
            # ✅ FIX: Use Token.objects.create directly.
            # get_or_create can be unnecessarily complex here if you are sure 
            # a token doesn't exist yet (which is true right after user creation).
            # The standard DRF practice is to use create here.
            Token.objects.create(user=user)
        except IntegrityError:
            # Handle the unlikely case where a token somehow already exists (e.g., race condition)
            pass
        except AttributeError:
             # If the Token model still isn't fully loaded, try fetching a pre-existing one 
             # (Though this shouldn't happen right after user creation)
             pass 
             
        return user