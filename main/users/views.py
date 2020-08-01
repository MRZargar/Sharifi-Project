from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomUserCreationForm2, CustomUserCreationForm3
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
from django.core.mail import EmailMultiAlternatives
from main.settings import EMAIL_HOST_USER
from django.utils.html import strip_tags
from django.http import JsonResponse
import stations.models as all_staions

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


@login_required(login_url='signpage')
def SignUpView(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomUserCreationForm3(request.POST, new_choices=(('is_user', 'user'),('is_operator', 'operator'),))
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            password = form.cleaned_data['password1']
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Geolab Account'
            from_email = EMAIL_HOST_USER
            message = render_to_string('account_activation_email2.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'password': password,
            })
            text_message = strip_tags(message)
            msg = EmailMultiAlternatives(subject, text_message, from_email, [str(user.email)])
            msg.attach_alternative(message, "text/html")
            msg.send()
            messages.success(request, "Please confirm your email address to complete the registration.")
            return redirect('signup', pk)
    else:
        form = CustomUserCreationForm3(new_choices=(('is_user', 'user'),('is_operator', 'operator'),))
    return render(request, 'signup.html', {'form': form})




@login_required(login_url='signpage')
def active_user_page(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    if request.method == 'POST':
        usernames = request.POST.getlist('UserNames[]')
        method = request.POST['Method']
        if method == "Active":
            for username in usernames:
                user = User.objects.get(username=username)
                user.admin_confirmed = True
                user.save()
        elif method == "Deactive":
            for username in usernames:
                user = User.objects.get(username=username)
                user.admin_confirmed = False
                user.active_email_send = False
                user.save()
        return JsonResponse({},status=200)
    else:
        users1 = User.objects.filter(userType='is_user').order_by('date_joined').reverse()
        users2 = User.objects.filter(userType='is_operator').order_by('date_joined').reverse()
        users = users2 | users1
        count_of_user = users.count()
        user_list = []
        for user in users:
            if user.userType == 'is_user':
                user_type = 'user'
            elif user.userType == 'is_operator':
                user_type = 'operator'
            user_list.append({'username': user.username, 'email': user.email, 'phone_number':user.phone_number, 'status' :user.admin_confirmed, 'user_type' : user_type})
        return JsonResponse({'user_list':user_list, 'count': count_of_user}, status=200)



@login_required(login_url='signpage')
def user_delete(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    if request.method == 'POST':
        usernames = request.POST.getlist('UserNames[]')
        for username in usernames:
            User.objects.get(username=username).delete()
        return JsonResponse({}, status=200)



@login_required(login_url='signpage')
def access_station(request, pk):
    obj = request.user
    if obj.userType != 'is_admin':
        raise PermissionDenied
    if request.method == 'POST':
        method = request.POST['Method']
        if method == "single_access":
            username = request.POST['UserName']
            user_access_list = request.POST.getlist('UserAcessList[]')
            count_of_access = len(user_access_list)
            my_user = User.objects.get(username=username)
            user_access = all_staions.Access.objects.filter(user = my_user)
            if user_access.count() == 0:
                for i in range(int(count_of_access/2)):
                    if user_access_list[i*2 + 1] == 'true':
                        my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                        all_staions.Access.objects.create(user=my_user, station=my_station)
                    elif user_access_list[i*2 + 1] == 'false':
                        continue
            else:
                user_accessed = all_staions.Access.objects.all()
                for i in range(int(count_of_access/2)):
                    if user_access_list[i*2 + 1] == 'true':
                        my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                        temp = True
                        for userAccess in user_accessed:
                            if userAccess.station == my_station:
                                if userAccess.user == my_user:
                                    temp = False
                        if temp:
                            all_staions.Access.objects.create(user=my_user, station=my_station)
                    elif user_access_list[i*2 + 1] == 'false':
                        my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                        temp = False
                        for userAccess in user_accessed:
                            if userAccess.station == my_station:
                                if userAccess.user == my_user:
                                    temp = True
                        if temp:
                            all_staions.Access.objects.get(user=my_user, station=my_station).delete()

            return JsonResponse({}, status=200)
        elif method == "multiple_access":
            usernames = request.POST.getlist('UserNames[]')
            user_access_list = request.POST.getlist('UserAcessList[]')
            count_of_access = len(user_access_list)
            for username in usernames:
                my_user = User.objects.get(username=username)
                user_access = all_staions.Access.objects.filter(user = my_user)
                if user_access.count() == 0:
                    for i in range(int(count_of_access/2)):
                        if user_access_list[i*2 + 1] == 'true':
                            my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                            all_staions.Access.objects.create(user=my_user, station=my_station)
                        elif user_access_list[i*2 + 1] == 'false':
                            continue
                else:
                    user_accessed = all_staions.Access.objects.all()
                    for i in range(int(count_of_access/2)):
                        if user_access_list[i*2 + 1] == 'true':
                            my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                            temp = True
                            for userAccess in user_accessed:
                                if userAccess.station == my_station:
                                    if userAccess.user == my_user:
                                        temp = False
                            if temp:
                                all_staions.Access.objects.create(user=my_user, station=my_station)
                        elif user_access_list[i*2 + 1] == 'false':
                            my_station = all_staions.Setup.objects.get(station_id=user_access_list[i*2])
                            temp = False
                            for userAccess in user_accessed:
                                if userAccess.station == my_station:
                                    if userAccess.user == my_user:
                                        temp = True
                            if temp:
                                all_staions.Access.objects.get(user=my_user, station=my_station).delete()

            return JsonResponse({}, status=200)

    else:
        username = request.GET['UserName']
        this_user = User.objects.get(username=username)
        stations = all_staions.Setup.objects.all().order_by('date').reverse()
        user_access = all_staions.Access.objects.filter(user = this_user)
        all_access = []
        stations_id = []
        for station in stations:
            temp = False
            stations_id.append(station.station_id)
            for access in user_access:
                if station == access.station:
                    temp = True
            if temp:
                all_access.append(True)
            else:
                all_access.append(False)
        count_of_station = len(stations_id)
        return JsonResponse({'stations_id': stations_id, 'access':all_access, 'count': count_of_station}, status=200)


@login_required(login_url='signpage')
def profile_view(request, pk):
    return render(request, 'profile.html', {})


def success_signup(request):
    return render(request, 'signup2.html', {})
@login_required(login_url='signpage')
def success_edit(request):
    return render(request, 'success_edit.html', {})


def SignUpView2(request):
    if request.method == 'POST':
        form = CustomUserCreationForm2(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Geolab Account'
            from_email = EMAIL_HOST_USER
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            text_message = strip_tags(message)
            msg = EmailMultiAlternatives(subject, text_message, from_email, [str(user.email)])
            msg.attach_alternative(message, "text/html")
            msg.send()
            messages.success(request, "Please confirm your email address to complete the registration.")
            return redirect('signup2')
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




