from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User


class UserLoginView(LoginView):
    template_name = "user_login.html"

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = "/user/login"
