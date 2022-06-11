import re
from django import forms
from django.forms import Form, ModelForm, CharField, PasswordInput, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import MemberModel

# class MemberFullForm(Form):
#     def clean_image(self):
#         image = self.cleaned_data.get('image', False)
#         if image:
#             if image._size > 4*1024*1024:
#                 raise ValidationError("Image file too large ( > 4mb )")
#             return image
#         else:
#             raise ValidationError("Couldn't read uploaded image")
#
# https://stackoverflow.com/a/6195783/


class UpdateForm(ModelForm):
	staff = forms.BooleanField(required=False, label="Staff")

	class Meta:
		model = MemberModel
		fields = ['name', 'surname', 'email', 'description', 'avatar']
	
	def __init__(self, *args, **kwargs):
		super(UpdateForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = False
		self.fields['surname'].required = False
		self.fields['email'].required = False
		self.fields['description'].required = False
		self.fields['avatar'].required = False

class RegisterForm(ModelForm):
    password = CharField(widget=PasswordInput())
    confirm_password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password(self):
        return make_password(self.cleaned_data.get('password'))

    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.data['confirm_password']

        if password != confirm_password:
            raise ValidationError('password confirmation does not match')
        return confirm_password


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())