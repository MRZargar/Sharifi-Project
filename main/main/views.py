from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os

def home_page(request):
    homePage_title = ""
    return render(request, "homePage.html", {'title':homePage_title})

'''
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect("profile")
        else:
            return render(request, 'signin2.html', {})
    return render(request, 'signin.html', {})
'''

def profile(request):
    if request.session.has_key('username'):
        posts = request.session['username']
        query = User.objects.filter(username=posts)
        return render(request, 'profile.html', {"query":query})
    else:
        return render(request, 'login.html', {})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'logout.html', {})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['username'] = username
            return redirect("profile")
        else:
            return render(request, 'login2.html', {})
    else:
        return render(request, 'login.html', {})

def plot_page(request):
    from .Functions import simplePlot
    filename = 'plot_test.html'
    cwd = os.getcwd()
    script, div = simplePlot.plot_data(filename, cwd)
    return render(request, 'plot.html', dict(script=script, div=div))
