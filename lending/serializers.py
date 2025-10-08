from rest_framework import serializers
from .models import LendingRequest
from users.serializers import UserSerializer
from items.serializers import ItemSerializer

class LendingRequestSerializer(serializers.ModelSerializer):
    borrower_details = UserSerializer(source='borrower', read_only=True)
    item_details = ItemSerializer(source='item', read_only=True)
    
    class Meta:
        model = LendingRequest
        fields = [
            'id', 'item', 'borrower', 'status', 'requested_from', 
            'requested_to', 'approved_at', 'returned_at', 'created_at',
            'updated_at', 'borrower_details', 'item_details'
        ]
        read_only_fields = ['borrower', 'approved_at', 'returned_at', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Get the item instance - either from validated data or existing instance
        item = data.get('item') or getattr(self.instance, 'item', None)
        requested_from = data.get('requested_from')
        requested_to = data.get('requested_to')
        
        # Basic date validation
        if requested_from and requested_to:
            if requested_from >= requested_to:
                raise serializers.ValidationError("End date must be after start date")
        
        # Item availability validation
        if item and requested_from and requested_to:
            # Check if item is available for lending
            if not item.is_available:
                raise serializers.ValidationError("This item is currently not available for lending")
            
            # Check for overlapping availability periods (when item is marked unavailable)
            overlapping_unavailable = item.availability_set.filter(
                unavailable_from__lte=requested_to,
                unavailable_to__gte=requested_from
            ).exists()
            
            if overlapping_unavailable:
                raise serializers.ValidationError("Item is not available for the requested dates")
            
            # Check for approved/pending lending requests that overlap
            # Exclude current instance if updating
            overlapping_requests = item.lending_requests.filter(
                status__in=['PENDING', 'APPROVED', 'ON_LOAN'],
                requested_from__lte=requested_to,
                requested_to__gte=requested_from
            )
            
            # If updating an existing instance, exclude it from the overlap check
            if self.instance:
                overlapping_requests = overlapping_requests.exclude(id=self.instance.id)
            
            if overlapping_requests.exists():
                raise serializers.ValidationError("Item already has pending or approved requests for these dates")
        
        return data