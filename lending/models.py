from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from items.models import Item  # Assuming Item model is in the 'items' app

# --- Status Choices ---
# Defines the lifecycle of a lending request, directly matching project requirements.
STATUS_CHOICES = [
    ('PENDING', 'Pending Owner Review'),
    ('APPROVED', 'Approved by Owner'),
    ('DENIED', 'Denied by Owner'),
    ('ON_LOAN', 'Currently on Loan'),
    ('COMPLETED', 'Completed and Returned'),
    ('CANCELED', 'Canceled by Borrower'),
]

class LendingRequest(models.Model):
    """
    Model to track the entire lending/borrowing transaction for an Item.
    """

    # --- Foreign Keys ---
    
    # The Item being requested. (FK to Item model in the 'items' app)
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='lending_requests',
        verbose_name='Requested Item',
    )
    
    # The user requesting to borrow the Item. (FK to the custom User model)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrowing_requests',
        verbose_name='Borrower',
    )
    
    # --- Transaction Dates ---
    
    # The date the borrower requested to pick up the item.
    requested_from = models.DateField(
        verbose_name='Requested Start Date',
        help_text='The date the borrower wants to pick up the item.',
    )
    
    # The date the borrower expects to return the item.
    requested_to = models.DateField(
        verbose_name='Requested End Date',
        help_text='The date the borrower expects to return the item.',
    )

    # --- Status and Timestamps ---

    # Current status of the lending request.
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Request Status',
    )
    
    # Timestamp when the request was approved by the owner. (Optional)
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Approval Timestamp',
    )
    
    # Timestamp when the item was marked as returned, completing the cycle. (Optional)
    returned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Return Timestamp',
    )

    # When the request was initially created. (Automated)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Created',
    )
    
    # When the request was last updated (e.g., status change). (Automated)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated',
    )

    # --- Metadata and Methods ---

    class Meta:
        verbose_name = 'Lending Request'
        verbose_name_plural = 'Lending Requests'
        ordering = ['-created_at']
        # Optional constraint to prevent a user from requesting the same item for overlapping dates
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['item', 'borrower', 'requested_from', 'requested_to'], 
        #         name='unique_lending_request'
        #     )
        # ]

    def __str__(self):
        """String representation for the Django Admin and debugging."""
        return f"Request for '{self.item.name}' by {self.borrower.username} - {self.status}"
    
    def save(self, *args, **kwargs):
        """Override save to auto-set timestamps based on status changes."""
        # Auto-set approved_at when status changes to approved
        if self.status == 'APPROVED' and not self.approved_at:
            self.approved_at = timezone.now()
        
        # Auto-set returned_at when status changes to completed
        if self.status == 'COMPLETED' and not self.returned_at:
            self.returned_at = timezone.now()
            
        super().save(*args, **kwargs)