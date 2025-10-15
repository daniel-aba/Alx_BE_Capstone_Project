from rest_framework import serializers
from django.utils import timezone
from .models import LendingRequest
# Import only the necessary serializers or none if only names are displayed
from users.serializers import UserSerializer 
from items.serializers import ItemSerializer

class LendingRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the LendingRequest model, including validation 
    for date ranges, availability, and user permissions.
    """
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
        # 'borrower' is set automatically in the view, so it's read-only here
        read_only_fields = ['borrower', 'approved_at', 'returned_at', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Main object-level validation:
        1. Ensure date range is valid (to > from) and not in the past.
        2. Ensure item owner is not the borrower.
        3. Perform item availability and date overlap checks.
        """
        
        # 1. Retrieve the validated date objects
        # We use data.get for creation, or getattr(self.instance, ...) for updates
        requested_from = data.get('requested_from', getattr(self.instance, 'requested_from', None))
        requested_to = data.get('requested_to', getattr(self.instance, 'requested_to', None))
        
        # 1a. Check if the dates conflict (requested_from must be strictly before requested_to)
        if requested_from and requested_to and requested_from >= requested_to:
            raise serializers.ValidationError({
                'requested_to': "Requested 'to' date must be after 'from' date."
            })
            
        # 1b. Check for past dates
        if requested_from and requested_from < timezone.localdate():
            raise serializers.ValidationError({
                'requested_from': "Cannot request an item for a past date."
            })

        # Get the item instance and request user
        item = data.get('item') or getattr(self.instance, 'item', None)
        request = self.context.get('request')
        
        # 2. Ensure item owner is not the borrower 
        if request and item and request.user == item.owner:
            # Check only for creation or if the item field is being updated
            if self.instance is None or 'item' in data:
                raise serializers.ValidationError("You cannot borrow your own item.")
        
        # 3. Item Availability and Overlap Validation
        if item and requested_from and requested_to:
            # Check if item is available for lending (global flag)
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
