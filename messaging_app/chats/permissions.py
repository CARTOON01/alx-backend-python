from rest_framework import permissions

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
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            # For Message objects
            return request.user in obj.conversation.participants.all()
        elif hasattr(obj, 'participants'):
            # For Conversation objects
            return request.user in obj.participants.all()
        return False

class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to only allow senders of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user 