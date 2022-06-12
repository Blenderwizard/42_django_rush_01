from django.urls import path

from . import views


urlpatterns = [
    # path('forum/', RegisterFormView.as_view(), name='register'),
	path('forum/', views.Forum.as_view(), name='forum'),
	path('forum/<int:pk>/', views.ForumDetail.as_view(), name='forum detail'),
	path('publish/', views.Publish.as_view(), name='publish')
]
