from django.urls import path

from . import views


urlpatterns = [
    # path('forum/', RegisterFormView.as_view(), name='register'),
	path('forum/', views.Forum.as_view(), name='forum;'),
	path('publish/', views.Publish.as_view(), name='publish')
]
