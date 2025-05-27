from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # AbstractUser already has email, password, first_name, last_name

    def __str__(self):
        return f"{self.username} ({self.email})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"Conversation {self.conversation_id}"
    
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