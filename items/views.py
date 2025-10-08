from rest_framework import viewsets
from .models import Item, Availability
from .serializers import ItemSerializer, AvailabilitySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Make sure this exists
    serializer_class = ItemSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()  # Make sure this exists
    serializer_class = AvailabilitySerializer