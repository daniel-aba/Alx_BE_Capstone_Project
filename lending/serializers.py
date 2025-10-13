from rest_framework import serializers
from .models import LendingRequest
# Import only the necessary serializers or none if only names are displayed
from users.serializers import UserSerializer 
from items.serializers import ItemSerializer

class LendingRequestSerializer(serializers.ModelSerializer):
    # Read-only fields for displaying related object details quickly
    borrower_username = serializers.CharField(source='borrower.username', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_owner_username = serializers.CharField(source='item.owner.username', read_only=True)

    class Meta:
        model = LendingRequest
        fields = [
            'id', 
            # Writable field for creation
            'item', 
            # Read-only details from related objects
            'item_name', 'item_owner_username', 
            'borrower', 'borrower_username', 
            # Writable date fields
            'requested_from', 'requested_to', 
            # CRUCIAL: 'status' must be writable for PATCH/PUT requests
            'status', 
            # Read-only timestamp fields
            'approved_at', 'returned_at', 
            'created_at', 'updated_at'
        ]
        # Keep 'borrower' read-only as it's set automatically in the view
        # Keep timestamps read-only as they are set by the database/view logic
        read_only_fields = ['borrower', 'approved_at', 'returned_at', 'created_at', 'updated_at']
    
    # --- Custom Validation Methods ---
    
    def validate_requested_to(self, value):
        """Custom validation for requested_to field."""
        # Check if requested_from is available in initial_data (for create) or instance (for update)
        requested_from = self.initial_data.get('requested_from')
        if not requested_from and self.instance:
            requested_from = self.instance.requested_from
            
        if requested_from and value <= requested_from:
            raise serializers.ValidationError("The return date must be after the requested start date.")
        return value

    def validate(self, data):
        """
        Main object-level validation:
        1. Ensure item owner is not the borrower.
        2. Perform item availability and date overlap checks.
        """
        # Get the item instance and request user
        item = data.get('item') or getattr(self.instance, 'item', None)
        request = self.context.get('request')
        
        # 1. Ensure item owner is not the borrower (only checked on creation/if item is updated)
        if request and item and request.user == item.owner:
            # Check only for creation or if the item field is being updated
            if self.instance is None or 'item' in data:
                raise serializers.ValidationError("You cannot borrow your own item.")
        
        # Get/default date fields for availability check
        requested_from = data.get('requested_from', getattr(self.instance, 'requested_from', None))
        requested_to = data.get('requested_to', getattr(self.instance, 'requested_to', None))
        
        # 2. Item Availability and Overlap Validation
        if item and requested_from and requested_to:
            # Check if item is available for lending (using the model's is_available field)
            if not item.is_available:
                raise serializers.ValidationError("This item is currently not available for lending.")
            
            # Check for overlapping unavailable periods marked by the owner
            overlapping_unavailable = item.availabilities.filter(
                unavailable_from__lte=requested_to,
                unavailable_to__gte=requested_from
            ).exists()
            
            if overlapping_unavailable:
                raise serializers.ValidationError("Item is not available for the requested dates due to owner's block.")
            
            # Check for approved/pending/on_loan lending requests that overlap
            overlapping_requests = item.lending_requests.filter(
                status__in=['PENDING', 'APPROVED', 'ON_LOAN'],
                requested_from__lte=requested_to,
                requested_to__gte=requested_from
            )
            
            # If updating an existing instance, exclude it from the overlap check
            if self.instance:
                overlapping_requests = overlapping_requests.exclude(id=self.instance.id)
            
            if overlapping_requests.exists():
                raise serializers.ValidationError("Item already has pending or approved requests for these dates.")
        
        return data