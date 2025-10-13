from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers # For ValidationError
from django.db import models
from django.utils import timezone # Needed for setting returned_at
from .models import LendingRequest
from .serializers import LendingRequestSerializer
# Assuming you moved IsOwnerOrBorrower to a permissions.py file:
# from .permissions import IsOwnerOrBorrower 
# If it's still in this file, you can remove the next line and uncomment the original definition.
from messaging.models import Message # Import the Message model!


# NOTE: If you haven't moved this class, keep it here.
# If you *have* moved it to permissions.py, delete this section 
# and uncomment the import at the top of the file.
class IsOwnerOrBorrower(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read/update access if the user is the borrower OR the item owner.
        return obj.borrower == request.user or obj.item.owner == request.user


class LendingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LendingRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrBorrower]

    def get_queryset(self):
        user = self.request.user
        # Show requests I made (borrower) OR requests for items I own (owner)
        return LendingRequest.objects.filter(
            models.Q(borrower=user) | models.Q(item__owner=user)
        ).select_related('borrower', 'item', 'item__owner').distinct()
    
    def perform_create(self, serializer):
        # Status automatically set to PENDING by the model's default.
        serializer.save(borrower=self.request.user)

    # Core logic for status changes and auto-messaging
    def perform_update(self, serializer):
        # Get the status before the update
        old_status = serializer.instance.status
        
        # Save the instance to apply the update (including status change)
        new_request = serializer.save()
        new_status = new_request.status

        # Only proceed with custom messaging/workflow if the status has actually changed
        if old_status != new_status:
            item_owner = new_request.item.owner
            borrower = new_request.borrower
            
            # --- Auto-Messaging & Workflow Logic ---

            # 1. OWNER Actions: APPROVED/DENIED
            if new_status in ['APPROVED', 'DENIED']:
                if self.request.user != item_owner:
                    # Non-owner attempting to approve/deny should raise an error
                    raise serializers.ValidationError({"status": "Only the item owner can approve or deny a request."})
                
                recipient = borrower
                sender = item_owner
                action_word = new_status.upper()
                content = f"Your request for '{new_request.item.name}' has been **{action_word}** by the owner."
            
            # 2. RETURN Action: COMPLETED
            elif new_status == 'COMPLETED':
                # The IsOwnerOrBorrower permission already restricts who can update the object.
                # This check ensures that only the borrower or the owner is making the call.
                if self.request.user != item_owner and self.request.user != borrower:
                    # Unreachable if permissions work, but good safeguard
                    raise serializers.ValidationError({"status": "Only the item owner or borrower can mark an item as returned."})
                
                # Manually set the return timestamp
                new_request.returned_at = timezone.now() 
                new_request.save() # Save needed for the timestamp field
                
                # Notify the person who *didn't* mark it complete
                recipient = item_owner if self.request.user == borrower else borrower
                sender = self.request.user
                content = f"The item '{new_request.item.name}' has been marked as **RETURNED** by {sender.username}."
            
            # 3. Create the Message object if a notification message was generated
            # Check if 'content' was set in the blocks above
            if 'content' in locals():
                Message.objects.create(
                    sender=sender,
                    recipient=recipient,
                    content=content,
                    # Optional: link the message directly to the lending request
                    # related_object=new_request # Requires a GenericForeignKey on Message model
                )
        
        # Final save for standard updates or the status change, ensures updated_at is set.
        # This call is already included implicitly by the initial serializer.save() at the start,
        # but calling super().perform_update(serializer) ensures standard DRF behaviour is followed 
        # for fields other than status that might have been updated.
        super().perform_update(serializer)