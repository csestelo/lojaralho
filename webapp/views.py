from django.conf import settings
from django.contrib.auth import login as log_user_in
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from webapp.forms import UserSignupForm, UserAuthenticationForm


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('welcome'))

    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            log_user_in(request, form.get_user())
            return HttpResponseRedirect(reverse('welcome'))
    else:
        form = UserAuthenticationForm
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            log_user_in(request, user)
            return HttpResponseRedirect(reverse('welcome'))
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


def welcome(request):
    return render(request, 'welcome.html', {'user': request.user})
