from rest.framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.Charfield(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']
        read_only_fields = ['message_id', 'sent_at', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    partcipants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']
        read_only_fields = ['conversation_id']
    
    def get_messages(self, obj):
        messages = obj.messages.all().order_by('-sent_at')
        return MessageSerializer(messages, many=True).data
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value