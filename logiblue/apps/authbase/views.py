from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse

from .forms import LoginForm, RegisterForm
from apps.user.models import User


class LoginView(View):
    template_name = 'authbase/login.html'
    context = {}
    form = LoginForm

    def get(self, request, *args, **kwagrs):
        self.context['form'] = self.form()
        self.context['messages'] = messages.get_messages(request)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            password = form.cleaned_data.get('password', None)
            user = authenticate(request, username=email, password=password)

            if user is None:
                messages.error(request, _("No active account found with the given credentials"))  # noqa
            else:
                login(request, user)
                return redirect(reverse('home'))

        self.context['form'] = form
        self.context['messages'] = messages.get_messages(request)
        return render(request, self.template_name, self.context)


class RegisterView(View):
    template_name = 'authbase/register.html'
    form = RegisterForm
    context = {}

    def get(self, request, *args, **kwagrs):
        self.context['form'] = self.form()
        self.context['messages'] = None
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name', None)
            email = form.cleaned_data.get('email', None)
            password = form.cleaned_data.get('password', None)

            User.objects.create_user(email=email, first_name=name, password=password)
            messages.success(request, _("Register success!"))
            return redirect(reverse('login'))

        self.context['form'] = form
        self.context['messages'] = messages.get_messages(request)
        return render(request, self.template_name, self.context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))
