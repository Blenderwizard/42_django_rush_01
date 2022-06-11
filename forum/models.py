from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CommentModel(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	content = models.TextField(blank=False)
	created = models.DateTimeField(blank=False, auto_now_add=True)
	comments = models.ManyToManyField('self', blank=True)
	id = models.IntegerField(primary_key=True)

class ForumModel(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	title = models.CharField(blank=False, max_length=64)
	content = models.TextField(blank=False)
	created = models.DateTimeField(blank=False, auto_now_add=True)
	comments = models.ManyToManyField(CommentModel, blank=True, related_name='article')
	id = models.IntegerField(primary_key=True)