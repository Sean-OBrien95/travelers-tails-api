from django.urls import path
from .views import MessageListCreateAPIView, MessageDetailAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view()),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view()),
]
