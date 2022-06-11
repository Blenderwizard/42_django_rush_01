from django.contrib import admin
from .models import MemberModel

# Register your models here.

class MemberModelAdmin(admin.ModelAdmin):
	model = MemberModel
	fields = ['user', 'name', 'surname', 'email', 'description', 'avatar']

admin.site.register(MemberModel, MemberModelAdmin)