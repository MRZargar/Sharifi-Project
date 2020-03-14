
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import render

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('sucess')
    template_name = 'signup.html'

def sucess_signup(request):
    return render(request, 'signup2.html', {})
