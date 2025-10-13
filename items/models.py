from django.db import models
from django.contrib.auth import get_user_model # RECOMMENDED: Import the utility function

# Get the custom user model defined by AUTH_USER_MODEL in settings.py
User = get_user_model() 

class Item(models.Model):
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]

    # Reference the User model using the variable assigned by get_user_model()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_items') 
    name = models.CharField(max_length=150)
    description = models.TextField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=100, help_text="Simplified location for pickup/return.")
    is_available = models.BooleanField(default=True, help_text="Quick status check for item availability.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.owner.username}"

# Availability model
class Availability(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='availabilities')
    unavailable_from = models.DateField()
    unavailable_to = models.DateField()

    class Meta:
        verbose_name_plural = "Availabilities"

    def __str__(self):
        return f"{self.item.name}: {self.unavailable_from} to {self.unavailable_to}"