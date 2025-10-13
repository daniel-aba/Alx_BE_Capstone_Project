from rest_framework import permissions

class IsOwnerOrBorrower(permissions.BasePermission):
    """
    Custom permission to only allow the owner of the item or the borrower
    to view or interact with the lending request associated with that item.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) are allowed for any involved user.
        if request.method in permissions.SAFE_METHODS:
            return obj.item.owner == request.user or obj.borrower == request.user

        # Write permissions (PATCH/PUT for status updates)
        # Only the item owner or the borrower should have write access.
        # The specific action restrictions (e.g., only owner can approve)
        # will be handled inside the ViewSet's perform_update method.
        return obj.item.owner == request.user or obj.borrower == request.user
