from django.views.generic import View, DetailView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import MemberModel
from chat.models import DiscussionModel, RecipientModel

def temp(request):  # Should we use generic view for all others views?
	if request.user.is_authenticated:
		if not MemberModel.objects.filter(user=request.user).exists():
			MemberModel.objects.create(user=request.user)
	context = {}
	return render(request, 'home.html', context)


class MemberDetailView(DetailView):
	model = MemberModel

	def get_object(self):
		return MemberModel.objects.filter(user=self.kwargs['pk']).first()

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('home'))
		if not MemberModel.objects.filter(user=self.kwargs['pk']).exists():
			return redirect(reverse('home'))
		return super().get(request, *args, **kwargs)


class UpdateInformationView(UpdateView):
	template_name = 'member/update.html'
	model = MemberModel
	form_class = UpdateForm

	def get_object(self):
		return MemberModel.objects.filter(user=self.kwargs['pk']).first()

	def get_success_url(self) -> str:
		return reverse('user info', kwargs={'pk': str(self.kwargs['pk'])})

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('home'))
		if not MemberModel.objects.filter(user=self.kwargs['pk']).exists():
			if request.user.id == self.kwargs['pk']:
				# Allow user created with admin panel
				MemberModel(user=request.user).save()
			else:
				return redirect(reverse('home'))
		if request.user.is_staff:
			pass
		elif User.objects.get(username=request.user).id != self.kwargs['pk']:
			return redirect(reverse('home'))
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UpdateInformationView, self).get_context_data(**kwargs)
		if not User.objects.filter(id = int(self.kwargs['pk'])).exists:
			return context
		user = User.objects.get(id = int(self.kwargs['pk']))
		context['userinfo'] = MemberModel.objects.get(user=user)
		context['is_staff'] = self.request.user.is_staff
		context['user_is_staff'] = user.is_staff
		return context

	def form_valid(self, form):
		if not self.request.user.is_authenticated:
			return super().form_invalid(form)
		if not User.objects.filter(id=self.kwargs['pk']).exists():
			return super().form_invalid(form)
		if self.request.user.is_staff:
			if 'staff' in form.cleaned_data:
				user = User.objects.get(id=int(self.kwargs['pk']))
				user.is_superuser = form.cleaned_data['staff']
				user.is_staff = form.cleaned_data['staff']
				user.save()
		elif User.objects.get(username=self.request.user).id != self.kwargs['pk']:
			return super().form_invalid(form)
		userinfo = MemberModel.objects.get(user=User.objects.get(username=self.request.user))
		if 'name' in form.cleaned_data and form.cleaned_data['name'] != '':
			userinfo.name = form.cleaned_data['name']
		if 'surname' in form.cleaned_data and form.cleaned_data['surname'] != '':
			userinfo.surname = form.cleaned_data['surname']
		if 'email' in form.cleaned_data and form.cleaned_data['email'] != None:
			userinfo.email = form.cleaned_data['email']
		if 'description' in form.cleaned_data and form.cleaned_data['description'] != '':
			userinfo.description = form.cleaned_data['description']
		if 'avatar' in form.cleaned_data and form.cleaned_data['avatar'] != None:
			userinfo.avatar = form.cleaned_data['avatar']
		userinfo.save()
		return super().form_valid(form)

class RegisterFormView(FormView):
	template_name = 'member/register.html'
	form_class = RegisterForm
	success_url = reverse_lazy('home')

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect(reverse('home'))
		return super().get(request, *args, **kwargs)

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			return redirect(reverse('home'))
		user = form.save()
		userinfo = MemberModel(user=user)
		userinfo.save()
		login(self.request, user)
		return redirect('/')


class LoginFormView(FormView):
    template_name = 'member/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            return redirect(reverse('home'))
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'invalid credentials')
            form.add_error('username', '')
            form.add_error('password', '')
            return super().form_invalid(form)


class CreateDiscussionView(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.filter(id=int(self.kwargs['pk']))

		if (not request.user.is_authenticated or not user.exists()) and user == request.user:
			return redirect(reverse('home'))
		user = user.first()
		discussion = DiscussionModel.objects.filter(recipientmodel__user__id=request.user.id)
		if not discussion.exists():
			discussion = DiscussionModel()
			discussion.save()
			RecipientModel(discussion=discussion, user=user).save()
			RecipientModel(discussion=discussion, user=request.user).save()
		else:
			discussion = discussion.first()

		return redirect('/chat/' + str(discussion.id))


class LogoutView(View):  # CSRF: fix with a token?
	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			logout(request)
		return redirect(reverse('home'))
