from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'created_at']
        read_only_fields = ['message_id', 'sent_at', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

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
