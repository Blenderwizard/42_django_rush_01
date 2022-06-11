from django.urls import path
# from . import consumers
from . import views

urlpatterns = [
    # path('chat/', views.ChatroomListView.as_view(), name='chat'),
    # path('chat/<int:pk>/', views.ChatroomDetailView.as_view(), name='chatroom'),
]

# wspatterns = [
#     path('ws/chat/<int:pk>/', consumers.ChatConsumer.as_asgi()),
# ]
