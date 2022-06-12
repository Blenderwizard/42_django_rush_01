from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import CommentModel, ForumModel
from .forms import CreateForumForm, CreateCommentForm
from member.models import MemberModel

# Create your views here.

class Forum(ListView):
	model = ForumModel
	template_name = "forum/forums.html"

	def get_context_data(self, **kwargs):
		context = super(Forum, self).get_context_data(**kwargs)
		context['object_list'] = Paginator(ForumModel.objects.order_by('-created'), 10).page(self.request.GET.get('page', 1))
		if self.request.user.is_authenticated:
			if MemberModel.objects.filter(user=self.request.user).exists():
				context['userinfo'] = MemberModel.objects.get(user=self.request.user)
			context['user'] = self.request.user
		return context

class ForumDetail(FormView):
	form_class = CreateCommentForm
	template_name = "forum/foruminfo.html"
	success_url = reverse_lazy('forum')

	def get_success_url(self) -> str:
		return super().get_success_url() + str(self.kwargs['pk'])

	def get(self, request, *args, **kwargs):
		if not ForumModel.objects.filter(id=int(self.kwargs['pk'])):
			return redirect(reverse('forum'))
		if self.request.user.is_authenticated:
			if not MemberModel.objects.filter(user=self.request.user).exists():
				MemberModel.objects.create(user=self.request.user)
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context =  super().get_context_data(**kwargs)
		context['forum'] = ForumModel.objects.get(id=int(self.kwargs['pk']))
		context['isuser'] = self.request.user.is_authenticated
		if self.request.user.is_authenticated:
			if MemberModel.objects.filter(user=self.request.user).exists():
				context['userinfo'] = MemberModel.objects.get(user=self.request.user)
		return context
	
	def form_valid(self, form):
		if not self.request.user.is_authenticated:
			return super().form_invalid(form)
		if 'content' not in form.cleaned_data:
			return super().form_invalid(form)
		if 'parrentForm' in self.request.POST and 'parrentComment' in self.request.POST:
			return super().form_invalid(form)
		if 'parrentForm' in self.request.POST and ForumModel.objects.filter(id=int(self.request.POST['parrentForm'])).exists():
			if not User.objects.filter(username=self.request.user).exists():
				return super().form_invalid(form)
			CommentModel.objects.create(
				author = User.objects.get(username=self.request.user), 
				content = form.cleaned_data['content'],
				userinfo = MemberModel.objects.get(user=self.request.user),
				shallow = ForumModel.objects.get(id=int(self.request.POST['parrentForm']))
			)
		elif 'parrentComment' in self.request.POST and CommentModel.objects.filter(id=int(self.request.POST['parrentComment'])).exists():
			if not User.objects.filter(username=self.request.user).exists():
				return super().form_invalid(form)
			CommentModel.objects.create(
				author = User.objects.get(username=self.request.user), 
				content = form.cleaned_data['content'],
				userinfo = MemberModel.objects.get(user=self.request.user),
				deep = CommentModel.objects.get(id=int(self.request.POST['parrentComment']))
			)
		return super().form_valid(form)

class Publish(CreateView):
	model = ForumModel
	form_class = CreateForumForm
	template_name = "forum/publish.html"
	success_url = reverse_lazy('forum')

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('home'))
		if self.request.user.is_authenticated:
			if not MemberModel.objects.filter(user=self.request.user).exists():
				MemberModel.objects.create(user=self.request.user)
		return super().get(request, *args, **kwargs)

	def form_valid(self, form):
		user = self.request.user
		userinfo = MemberModel.objects.get(user=self.request.user)
		form.instance.author = user
		form.instance.userinfo = userinfo
		return super(Publish, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(Publish, self).get_context_data(**kwargs)
		context['isuser'] = self.request.user.is_authenticated
		if self.request.user.is_authenticated:
			context['username'] = self.request.user
		return context

