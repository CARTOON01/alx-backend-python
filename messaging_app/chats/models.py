from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.email})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    participants = models.ManyToManyField(
        User,
        related_name='conversations')

    def __str__(self):
        return f"Conversation {self.conversation_id}"
    
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
         User,
         on_delete=models.CASCADE,
         related_name='messages'
     )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
