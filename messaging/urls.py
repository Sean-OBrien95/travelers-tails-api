from django.urls import path
from .views import CustomInbox, CustomGetMessages, CustomSendMessages

urlpatterns = [
    path('inbox/<int:user_id>/', CustomInbox.as_view()),
    path('messages/<int:sender_id>/<int:receiver_id>/', CustomGetMessages.as_view()),
    path('send/', CustomSendMessages.as_view()),
]
