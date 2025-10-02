# users/serializers.py 
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'location', 'profile_picture']
        read_only_fields = ['id']
        # Security Note: 'password' is not included here for retrieval/listing.
        # A separate serializer would be used for registration to handle hashing.