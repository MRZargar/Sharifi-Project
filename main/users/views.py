
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserCreationForm2
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from .models import CustomUser
from django.core.exceptions import PermissionDenied
class AuthorUpdate(UpdateView):
    model = CustomUser
    fields = ['username']
    success_url = reverse_lazy('success_edit')
    template_name = 'update_form.html'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('success')
    template_name = 'signup.html'
    def dispatch(self, request, *args, **kwargs):
        obj = self.request.user
        print(obj)
        if obj.userType != 'is_admin':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

def success_signup(request):
    return render(request, 'signup2.html', {})

def success_edit(request):
    return render(request, 'success_edit.html', {})



class SignUpView2(CreateView):
    form_class = CustomUserCreationForm2
    success_url = reverse_lazy('signpage')
    template_name = 'signupUser.html'