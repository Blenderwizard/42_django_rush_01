from django.urls import path
from . import views
from .views import RegisterFormView, LoginFormView, LogoutView, UpdateInformationView

urlpatterns = [
    path('', views.temp, name='home'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('user/<int:pk>', UpdateInformationView.as_view(), name='user info')
]
