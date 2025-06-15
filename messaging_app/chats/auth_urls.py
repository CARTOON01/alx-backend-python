from django.urls import path
from .auth import RegisterView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
]
