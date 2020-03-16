from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os
from django.contrib.auth import get_user_model
from users.models import CustomUser

User = get_user_model()

def home_page(request):
    homePage_title = ""
    return render(request, "Signin.html", {'title':homePage_title})




def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'Home.html', {"query":query})
    else:
        return render(request, 'Signin.html', {})

def signout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'signout.html', {})

def signpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            if user.is_user:
                if request.session.has_key('username'):
                    posts = request.session['username']
                    query = User.objects.filter(username=posts)
                return render(request, 'UserHome.html', {"query":query[0]})
            elif user.is_operator:
                if request.session.has_key('username'):
                    posts = request.session['username']
                    query = User.objects.filter(username=posts)
                    return render(request, 'OperatorHome.html', {"query":query[0]})
            elif user.is_admin:
                if request.session.has_key('username'):
                    posts = request.session['username']
                    query = User.objects.filter(username=posts)
                    return render(request, 'AdminHome.html', {"query":query[0]})
        else:
            return render(request, 'Signin2.html', {})
    else:
        return render(request, 'Signin.html', {})

def plot_page(request):
    print(request.GET['a'])
    from .Functions import simplePlot
    cwd = os.getcwd()
    script, div = simplePlot.plot_data(cwd)
    return render(request, 'plot.html', dict(script=script, div=div))

def plots_map_page(request):
    from .Functions import simplePlot
    cwd = os.getcwd()
    script, div = simplePlot.plot_map(cwd)
    return render(request, 'plot.html', dict(script=script, div=div))
