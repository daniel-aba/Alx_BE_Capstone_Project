from rest_framework import serializers
from rest_framework.authtoken.models import Token # Import Token model
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

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
        # Use make_password to hash the password securely before saving
        validated_data['password'] = make_password(validated_data['password'])
        # Create the user instance
        user = super().create(validated_data)
        
        # Create an authentication token for the new user
        # This makes the user instantly logged in after registration
        Token.objects.get_or_create(user=user)
        return user
