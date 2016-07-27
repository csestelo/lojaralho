from django.conf import settings
from django.contrib.auth import login as log_user_in
from django.core.urlresolvers import reverse
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
            user = form.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            log_user_in(request, user)
            return HttpResponseRedirect(reverse('welcome'))
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def welcome(request):
    return render(request, 'welcome.html', {'user': request.user})
