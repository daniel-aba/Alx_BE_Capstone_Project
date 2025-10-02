from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
       # Additional fields for user profile
    bio = models.TextField(blank=True, null=True, help_text="A brief bio about the user.")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="User's general location or neighborhood.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # We don't need to explicitly add username, email, password, etc.,
    # as they are inherited from AbstractUser.

    def __str__(self):
        return self.username
    