from django.db import models
from django.contrib.auth.models import User


class MemberModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True)
    surname = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='avatars')  # Do we use Pillow to reduce Image ?
