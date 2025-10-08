from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
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
        return LendingRequest.objects.filter(
            models.Q(borrower=user) | models.Q(item__owner=user)
        ).select_related('borrower', 'item', 'item__owner').distinct()
    
    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        lending_request = self.get_object()
        
        if lending_request.item.owner != request.user:
            return Response(
                {"error": "Only the item owner can approve requests"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        lending_request.status = 'approved'
        lending_request.save()
        
        serializer = self.get_serializer(lending_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def deny(self, request, pk=None):
        lending_request = self.get_object()
        
        if lending_request.item.owner != request.user:
            return Response(
                {"error": "Only the item owner can deny requests"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        lending_request.status = 'denied'
        lending_request.save()
        
        serializer = self.get_serializer(lending_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def mark_returned(self, request, pk=None):
        lending_request = self.get_object()
        
        if lending_request.item.owner != request.user and lending_request.borrower != request.user:
            return Response(
                {"error": "Only the item owner or borrower can mark as returned"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        lending_request.status = 'completed'
        lending_request.save()
        
        serializer = self.get_serializer(lending_request)
        return Response(serializer.data)