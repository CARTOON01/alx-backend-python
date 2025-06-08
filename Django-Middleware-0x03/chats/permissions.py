from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access its messages.
    This permission ensures that:
    1. Only authenticated users can access the API
    2. Only participants in a conversation can send, view, update and delete messages
    """
    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
            
        # For nested routes, check if user is participant in the conversation
        conversation_id = view.kwargs.get('conversation_pk')
        if conversation_id:
            from .models import Conversation
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
                if request.user not in conversation.participants.all():
                    if request.method in ["PUT", "PATCH", "DELETE", "GET", "POST"]:
                        raise PermissionDenied("You are not a participant of this conversation")
                    return False
            except Conversation.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            # For Message objects
            is_participant = request.user in obj.conversation.participants.all()
            if not is_participant and request.method in ["PUT", "PATCH", "DELETE"]:
                raise PermissionDenied("Only participants can modify messages in this conversation")
            return is_participant
        elif hasattr(obj, 'participants'):
            # For Conversation objects
            is_participant = request.user in obj.participants.all()
            if not is_participant and request.method in ["PUT", "PATCH", "DELETE"]:
                raise PermissionDenied("Only participants can modify this conversation")
            return is_participant
        return False

class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to only allow senders of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Only message senders can update or delete messages
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.sender == request.user
        return True