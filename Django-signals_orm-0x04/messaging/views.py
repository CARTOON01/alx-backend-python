from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.views.decorators import require_POST
from django.contrib.auth.decorators import login_required
from .models import Message, Notification, MessageHistory
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decoratorfrom .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer

User = get_user_model()

@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Redirect to a suitable page after deletion

@cache_page(60) # Cache the view for 60 seconds
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, 'messaging/conversation.html', {'messages': messages})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show messages where the user is sender or receiver
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def get_threaded_conversations(root_message_id):
        root_message = (
            Message.objects
            .select_related('sender', 'receiver', 'parent_message')
            .prefetch_related('replies__sender', 'replies__receiver')
            .get(id=root_message_id)
        )
        return root_message

    def get_message_thread(message):
        thread = {
            'id': message.id,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.content,
            'timestamp': message.timestamp,
            'replies': []
        }
        for reply in message.replies.all().select_related('sender', 'receiver'):
            thread['replies'].append(get_message_thread(reply))
        return thread

    def unread_inbox(request):
        user = request.user
        unread_messages = Message.unread.for_user(user)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show notifications for the logged-in user
        return Notification.objects.filter(user=self.request.user)

class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageHistory.objects.all().order_by('-edited_at')
    serializer_class = MessageHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show edit history for messages the user sent
        user = self.request.user
        return MessageHistory.objects.filter(message__sender=user)


@method_decorator(cache_page(60), name='dispatch')
class ConversationMessagesView(ListView):
    model = Message
    template_name = 'messages/conversation.html'
    context_object_name = 'message'

    def queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs['conversation_id']).order_by('timestamp')
