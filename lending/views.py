from rest_framework import viewsets
from .models import LendingRequest
from .serializers import LendingRequestSerializer

class LendingRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LendingRequestSerializer
    queryset = LendingRequest.objects.all()  # Required for DRF router
    
    def get_queryset(self):
        # Override to optimize queries with select_related
        return LendingRequest.objects.select_related('borrower', 'item')
    
    def perform_create(self, serializer):
        # Automatically set the borrower to the current user
        serializer.save(borrower=self.request.user)