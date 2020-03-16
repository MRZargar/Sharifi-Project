from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os
from django.contrib.auth import get_user_model
from users.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib import auth


User = get_user_model()

def home_page(request):
    return render(request, "Signin.html")




def UserProfile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'UserHome.html', {"query":query})
    else:
        return render(request, 'Signin.html', {})


def OperatorProfile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'OperatorHome.html', {"query":query})
    else:
        return render(request, 'Signin.html', {})


def AdminProfile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'AdminHome.html', {"query":query})
    else:
        return render(request, 'Signin.html', {})  



def signpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            if user.is_user:
                auth.login(request, user)
                return redirect("UserProfile")
            elif user.is_operator:
                    auth.login(request, user)
                    return redirect("OperatorProfile")
            elif user.is_admin:
                    auth.login(request, user)
                    return redirect("AdminProfile")
        else:
            return render(request, 'Signin2.html', {})
    else:
        return render(request, 'Signin.html', {})


def signout(request):
    auth.logout(request)
    return render(request,'signout.html')


def plot_page(request):
    from .Functions import simplePlot
    cwd = os.getcwd()
    script, div = simplePlot.plot_data(cwd)
    return render(request, 'plot.html', dict(script=script, div=div))

def plots_map_page(request):
    from .Functions import simplePlot
    cwd = os.getcwd()
    script, div = simplePlot.plot_map(cwd)
    return render(request, 'plot.html', dict(script=script, div=div))
    
# def my_handler404(request, exception):
#     return render(request, '404.html', status=404)