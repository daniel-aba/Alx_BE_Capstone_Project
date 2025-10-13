from django.db import models
from django.conf import settings # Recommened for referencing the User model

class Message(models.Model):
    # Sender is the ForeignKey to the User model (the user sending the message)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    # Recipient is the other ForeignKey (the user receiving the message)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-time_stamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"From: {self.sender.username} to {self.recipient.username} - {self.time_stamp.strftime('%Y-%m-%d %H:%M')}"