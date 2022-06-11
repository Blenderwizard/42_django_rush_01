from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from .forms import LoginForm, RegisterForm


def temp(request):  # Should we use generic view for all others views?
    context = {}
    return render(request, 'home.html', context)


class RegisterFormView(FormView):
    template_name = 'member/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
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


class LogoutView(View):  # CSRF: fix with a token?
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('home'))
