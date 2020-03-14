
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
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


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {
#         'form': form
#     })

# from django.contrib.auth.decorators import login_required

# # @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, ('Your password was successfully updated!'))
#             return redirect('accounts:change_password')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {
#         'form': form
#     })