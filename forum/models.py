from django.db import models
from django.contrib.auth.models import User
from member.models import MemberModel

# Create your models here.

class ForumModel(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	userinfo = models.ForeignKey(MemberModel, on_delete=models.CASCADE, blank=False)
	title = models.CharField(blank=False, max_length=64)
	content = models.TextField(blank=False)
	created = models.DateTimeField(blank=False, auto_now_add=True)
	id = models.IntegerField(primary_key=True)

class CommentModel(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	userinfo = models.ForeignKey(MemberModel, on_delete=models.CASCADE, blank=False)
	content = models.TextField(blank=False)
	created = models.DateTimeField(blank=False, auto_now_add=True)
	deep = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
	shallow = models.ForeignKey(ForumModel, blank=True, null=True, on_delete=models.CASCADE)
	id = models.IntegerField(primary_key=True)