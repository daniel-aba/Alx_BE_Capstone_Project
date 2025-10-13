from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Read-only fields to show context, not for creation/update
    sender_username = serializers.ReadOnlyField(source='sender.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Message
        # Fields for reading (GET)
        fields = [
            'id', 'sender', 'recipient', 'sender_username',
            'recipient_username', 'content', 'time_stamp', 'is_read'
        ]
        # Fields that should only be written (POST)
        read_only_fields = ['sender', 'time_stamp']

    def create(self, validated_data):
        # Automatically set the sender to the authenticated user
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)