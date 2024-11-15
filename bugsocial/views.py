from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # verify the user’s credentials and return a
            # User object representing the authenticated user if validation succeeds.
            user = authenticate(
                request, username=data['username'], password=data['password'])

            if user is not None:
                if user.is_active:
                    # set the user in the session
                    login(request, user)
                    return HttpResponse('Authentication successful')
                else:
                    return HttpResponse('Account disabled')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'bugsocial/login.html', {'form': form})
