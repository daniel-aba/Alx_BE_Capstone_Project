# users/views.py 
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    # Provides CRUD functionality for the User model
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
  