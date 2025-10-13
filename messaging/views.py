from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    # Only authenticated users can access messages
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Only show messages where the authenticated user is either the sender OR the recipient
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    # Custom action to retrieve a single message and mark it as read
    @action(detail=True, methods=['get'])
    def retrieve_and_mark_read(self, request, pk=None):
        message = self.get_object()

        # Check permission: Only sender or recipient can view
        if message.sender != request.user and message.recipient != request.user:
            return Response({"detail": "Not authorized to view this message."}, status=403)

        # Mark as read if the current user is the recipient and it's unread
        if message.recipient == request.user and not message.is_read:
            message.is_read = True
            message.save()

        serializer = self.get_serializer(message)
        return Response(serializer.data)