from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
        return render(request, 'homePage.html', {"query":query})
    else:
        return render(request, 'login.html', {})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return render(request, 'homePage.html', {})
        else:
            return render(request, 'login2.html', {})
    else:
        return render(request, 'login.html', {})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'logout.html', {})
