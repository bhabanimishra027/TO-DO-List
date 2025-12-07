# todo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import models
from django.contrib.auth.decorators import login_required

def home(request):
    # Landing page: if already logged in, go to the todo page
    if request.user.is_authenticated:
        return redirect('/todopage/')
    return render(request, 'signup.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        email = request.POST.get('emailid')
        password = request.POST.get('pwd')

        if not username or not password:
            return render(request, 'signup.html', {'error': 'Username and password are required.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('/login/')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todopage/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

    return render(request, 'login.html')


@login_required(login_url='/login/')
def todo(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        if title:
            models.Todoo.objects.create(title=title, user=request.user)
        return redirect('/todopage/')

    res = models.Todoo.objects.filter(user=request.user).order_by('-date')
    completed_count = res.filter(status=True).count()
    return render(request, 'todo.html', {'res': res, 'completed_count': completed_count})



@login_required(login_url='/login/')
def delete_todo(request, srno):
    obj = get_object_or_404(models.Todoo, srno=srno)
    if obj.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this task.")
    obj.delete()
    return redirect('/todopage/')


@login_required(login_url='/login/')
def edit_todo(request, srno):
    obj = get_object_or_404(models.Todoo, srno=srno)
    if obj.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this task.")

    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        if title:
            obj.title = title
            obj.save()
            return redirect('/todopage/')
        else:
            return render(request, 'edit_todo.html', {'obj': obj, 'error': 'Title cannot be empty.'})

    return render(request, 'edit_todo.html', {'obj': obj})


def signout(request):
    logout(request)
    return redirect('/login/')
