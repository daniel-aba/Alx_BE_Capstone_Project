from rest_framework import serializers
from rest_framework.authtoken.models import Token # Import Token model
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Field to hold the token after creation (read-only)
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
            'is_id_verified': {'read_only': True},
            'is_phone_verified': {'read_only': True},
            'national_id': {'write_only': True} # Keep sensitive fields write-only
        }

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        
        # Create an authentication token for the new user
        Token.objects.get_or_create(user=user)
        return user
