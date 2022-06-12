from django.urls import path
from . import views
from .views import RegisterFormView, LoginFormView, LogoutView, UpdateInformationView, MemberDetailView,\
    CreateDiscussionView

urlpatterns = [
    path('', views.temp, name='home'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('user/<int:pk>/', MemberDetailView.as_view(), name='user'),
	path('user/<int:pk>/edit', UpdateInformationView.as_view(), name='user info'),
	path('user/<int:pk>/mp', CreateDiscussionView.as_view(), name='create_conv')
]
