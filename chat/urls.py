from django.urls import path
# from . import consumers
from . import views

urlpatterns = [
    path('chat/', views.DiscussionListView.as_view(), name='discussions'),
    path('chat/<int:pk>/', views.DiscussionDetailView.as_view(), name='conv'),
]

# wspatterns = [
#     path('ws/chat/<int:pk>/', consumers.ChatConsumer.as_asgi()),
# ]
