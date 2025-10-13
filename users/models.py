from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Validator for common phone number formats (adjust as needed for your region)
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', 
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class User(AbstractUser): # <--- CLASS NAME CHANGED FROM 'User' TO 'CustomUser'
    # --- Existing fields retained ---
    bio = models.TextField(blank=True, null=True, help_text="A brief bio about the user.")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="User's general location or neighborhood.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # --- New fields added ---
    national_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True, 
        null=True,
        help_text="National Identification Number for verification."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17, 
        unique=True,
        blank=True, 
        null=True, 
        help_text="Primary contact phone number for the user."
    )
    
    # Fields for verification status
    is_id_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # We don't need to explicitly add username, email, password, etc.,
    # as they are inherited from AbstractUser.

    def __str__(self):
        return self.username