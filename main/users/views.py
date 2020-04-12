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
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

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

# class SignUpView(CreateView):
#     model = CustomUser
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('success')
#     template_name = 'signup.html'
#     def dispatch(self, request, *args, **kwargs):
#         obj = self.request.user
#         if obj.userType != 'is_admin':
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)


def SignUpView(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signupUser.html', {'form': form})










def success_signup(request):
    return render(request, 'signup2.html', {})

def success_edit(request):
    return render(request, 'success_edit.html', {})

# class SignUpView2(CreateView):
#     model = CustomUser
#     form_class = CustomUserCreationForm2
#     print('here is the model')
#     print(model.objects.all())
#     success_url = reverse_lazy('signpage')
#     template_name = 'signupUser.html'

def SignUpView2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm2(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm2()
    return render(request, 'signupUser.html', {'form': form})



def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('signpage')
    else:
        return render(request, 'account_activation_invalid.html')