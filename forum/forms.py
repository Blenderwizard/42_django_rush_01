from django import forms
from django.forms import ModelForm
from .models import ForumModel, CommentModel

class CreateForumForm(ModelForm):
	class Meta:
		model = ForumModel
		fields = ['title', 'content']

class CreateCommentForm(ModelForm):
	class Meta:
		model = CommentModel
		fields = ['content']