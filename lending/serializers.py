from rest_framework import serializers
from .models import LendingRequest

class LendingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingRequest
        fields = '__all__'
        read_only_fields = ['borrower', 'approved_at', 'returned_at', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data['requested_from'] >= data['requested_to']:
            raise serializers.ValidationError("End date must be after start date")
        return data