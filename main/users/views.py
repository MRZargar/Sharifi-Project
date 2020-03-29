
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserCreationForm2
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('sucess')
    template_name = 'signup.html'

def sucess_signup(request):
    return render(request, 'signup2.html', {})


class SignUpView2(CreateView):
    form_class = CustomUserCreationForm2
    success_url = reverse_lazy('signpage')
    template_name = 'signupUser.html'