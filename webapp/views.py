from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from webapp.forms import User as UserForm


def index(request):
    return render(request, 'index.html')


def login(request):
    pass


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})
