from django.forms import ModelForm
from .models import MessageModel


class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = ['content']
