from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, ListView

from .models import CommentModel, ForumModel
from .forms import CreateForumForm, CreateCommentForm

# Create your views here.

class Forum(ListView):
	model = ForumModel
	template_name = "forum/forums.html"

	def get_context_data(self, **kwargs):
		context = super(Forum, self).get_context_data(**kwargs)
		context['object_list'] = ForumModel.objects.order_by('-created')
		if self.request.user.is_authenticated:
			context['user'] = self.request.user
		return context

class Publish(CreateView):
	model = ForumModel
	form_class = CreateForumForm
	template_name = "forum/publish.html"
	success_url = "/forum"

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('home'))
		return super().get(request, *args, **kwargs)

	def form_valid(self, form):
		user = self.request.user
		form.instance.author = user
		return super(Publish, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(Publish, self).get_context_data(**kwargs)
		context['isuser'] = self.request.user.is_authenticated
		if self.request.user.is_authenticated:
			context['username'] = self.request.user
		return context

