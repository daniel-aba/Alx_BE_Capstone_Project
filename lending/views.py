from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers 
from django.db import models
from django.utils import timezone
from .models import LendingRequest
from .serializers import LendingRequestSerializer
from messaging.models import Message # Import the Message model

# -------------------------------------------------------------
# STEP 1: Custom Permission Class (Replaced IsOwnerOrBorrower)
# -------------------------------------------------------------

class IsItemOwnerOrRequester(permissions.BasePermission):
    """
    Custom permission to control access to LendingRequest objects.
    - Allows read access (GET) to anyone authenticated.
    - Allows updates (PATCH/PUT) only if the user is the item owner 
      or the request borrower.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read access (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the item owner or the request borrower
        is_owner = obj.item.owner == request.user
        is_requester = obj.borrower == request.user
        
        return is_owner or is_requester

class LendingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LendingRequestSerializer
    # Use the new, more specific permission class
    permission_classes = [permissions.IsAuthenticated, IsItemOwnerOrRequester]

    def get_queryset(self):
        user = self.request.user
        # Show requests I made (borrower) OR requests for items I own (owner)
        return LendingRequest.objects.filter(
            models.Q(borrower=user) | models.Q(item__owner=user)
        ).select_related('borrower', 'item', 'item__owner').distinct()
    
    def perform_create(self, serializer):
        # Automatically sets the borrower and initial status
        serializer.save(borrower=self.request.user, status='PENDING')

    # -----------------------------------------------------------------
    # STEP 2: Implement Status Change and Auto-Messaging Logic in update()
    # -----------------------------------------------------------------
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        old_status = instance.status
        
        # Save the instance to apply the update (calls perform_update internally)
        self.perform_update(serializer) 
        
        new_status = instance.status
        
        # Initialize content to None
        content = None
        sender = None
        recipient = None

        # --- Auto-Messaging Logic (Triggered only if status changed) ---
        if old_status != new_status:
            item_name = instance.item.name
            
            # 1. OWNER Actions: APPROVED/DENIED
            if new_status in ['APPROVED', 'DENIED']:
                # Ensure only the item owner can trigger these critical status changes
                if self.request.user != instance.item.owner:
                    # Raise a validation error if a non-owner tries to approve/deny
                    raise serializers.ValidationError({"status": "Only the item owner can approve or deny a request."})
                
                recipient = instance.borrower
                sender = instance.item.owner
                action_word = new_status.upper()
                
                content = f"Your request for '{item_name}' has been **{action_word}** by the owner."
            
            # 2. RETURN Action: COMPLETED (Can be triggered by owner or borrower)
            elif new_status == 'COMPLETED':
                
                # Set returned_at timestamp if not already set
                if not instance.returned_at:
                    instance.returned_at = timezone.now() 
                    # Use update_fields to save only the changed field
                    instance.save(update_fields=['returned_at']) 
                
                # Determine who gets notified (the person who didn't mark it complete)
                if request.user == instance.borrower:
                    recipient = instance.item.owner # Borrower notified owner
                    sender = instance.borrower
                    actor = "the borrower"
                else:
                    recipient = instance.borrower # Owner notified borrower
                    sender = instance.item.owner
                    actor = "the owner"
                
                content = f"The item '{item_name}' has been marked as **RETURNED** by {actor}."
            
            # 3. CANCELLED Action (Usually triggered by borrower)
            elif new_status == 'CANCELLED':
                # Notify the owner that the borrower cancelled
                recipient = instance.item.owner
                sender = instance.borrower
                content = f"The request for '{item_name}' was CANCELLED by the borrower."

            # 4. Create the Message object if 'content' was successfully generated
            if content and sender and recipient:
                Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                )

        # Return the response data
        return Response(serializer.data)
