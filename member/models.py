from django.db import models
from django.contrib.auth.models import User


class MemberModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True)
    surname = models.CharField(max_length=32, null=True)
    email = models.EmailField(null=True)
    description = models.TextField(null=True)
    avatar = models.ImageField(null=True)  # Do we use Pillow to reduce Image ?
