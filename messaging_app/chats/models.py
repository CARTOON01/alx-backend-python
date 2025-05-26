from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # You can add additional fields here if needed
    pass

class Conversation(models.Model):
    """
    Multiple users can be part of a conversation.
    """
    partcipants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"
    
class Message(models.Model):
     """
    A message sent in a conversation by a user.
    """
     
     sender = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE,
         related_name='messages'
     )

     conversation = models.ForeignKey(
            Conversation,
            on_delete=models.CASCADE,
            related_name='messages'
     )
     content = models.TextField()
     timestamp = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"Message from {self.sender.username} at {self.timestamp}"