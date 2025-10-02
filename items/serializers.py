# items/serializers.py 
from rest_framework import serializers
from .models import Item, Availability

class ItemSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username') # Read-only field for owner's username

    class Meta:
        model = Item
        fields = ['id', 'owner', 'owner_username', 'name', 'description', 'condition', 'location', 'is_available', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner_username']
        # Note: 'owner' will typically be set automatically on creation/update based on the logged-in user.

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'item', 'unavailable_from', 'unavailable_to']