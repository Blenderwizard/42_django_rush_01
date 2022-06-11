from django.forms import ModelForm
from .models import DiscussionModel


class DiscussionForm(ModelForm):
    class Meta:
        model = DiscussionModel
        fields = ['content']
