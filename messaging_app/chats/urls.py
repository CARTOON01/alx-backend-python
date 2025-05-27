from rest_franework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls'))
]
