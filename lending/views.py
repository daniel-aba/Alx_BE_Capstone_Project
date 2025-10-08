from rest_framework import viewsets, permissions
from .models import LendingRequest
from .serializers import LendingRequestSerializer

class IsOwnerOrBorrower(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.borrower == request.user or obj.item.owner == request.user

class LendingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LendingRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrBorrower]
    
    def get_queryset(self):
        user = self.request.user
        return LendingRequest.objects.filter(borrower=user) | LendingRequest.objects.filter(item__owner=user)
    
    # Update the get_queryset method in LendingRequestViewSet
def get_queryset(self):
    user = self.request.user
    return LendingRequest.objects.filter(
        models.Q(borrower=user) | models.Q(item__owner=user)
    ).select_related('borrower', 'item', 'item__owner').distinct()
    
    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)