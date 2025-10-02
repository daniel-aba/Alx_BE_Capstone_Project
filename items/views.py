# items/views.py 
from rest_framework import viewsets
from .models import Item, Availability
from .serializers import ItemSerializer, AvailabilitySerializer

class ItemViewSet(viewsets.ModelViewSet):
    # Provides CRUD functionality for the Item model
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer

    # Override perform_create to automatically set the owner to the logged-in user
    def perform_create(self, serializer):
        # The owner must be set to the user making the request (request.user)
        serializer.save(owner=self.request.user)

class AvailabilityViewSet(viewsets.ModelViewSet):
    # Provides CRUD functionality for the Availability model
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer