from django.contrib import admin
from .models import ForumModel, CommentModel

# Register your models here.

class ForumModelAdmin(admin.ModelAdmin):
	model = ForumModel
	fields = ['author', 'title', 'content', 'id']

admin.site.register(ForumModel, ForumModelAdmin)

class CommentModelAdmin(admin.ModelAdmin):
	model = CommentModel
	fields = ['author', 'content', 'shallow', 'deep','id']

admin.site.register(CommentModel, CommentModelAdmin)