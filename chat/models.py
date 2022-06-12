from django.db import models
from django.contrib.auth.models import User


class DiscussionModel(models.Model):
    title = models.CharField(max_length=64, null=True)


class RecipientModel(models.Model):
    discussion = models.ForeignKey(DiscussionModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MessageModel(models.Model):
    discussion = models.ForeignKey(DiscussionModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
