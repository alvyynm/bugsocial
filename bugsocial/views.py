from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import LoginForm, SignupForm, UserEditForm, ProfileEditForm
from .models import Contact, Profile
from actions.utils import create_action
# Create your views here.


def user_login(request):
    # if user is logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

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
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Account disabled')
            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = LoginForm()

    return render(request, 'bugsocial/login.html', {'form': form})


@login_required
def dashboards(request):
    return render(request, 'bugsocial/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    # if user is logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        user_form = SignupForm(request.POST)

        if user_form.is_valid():
            # create a new user obj without saving
            new_user = user_form.save(commit=False)
            # hash the user password and set it to the new user object
            new_user.set_password(user_form.cleaned_data['password'])
            # save the new user
            new_user.save()

            # create a corresponding profile object
            Profile.objects.create(user=new_user)
            # create a new action
            create_action(new_user, 'has created an account')
            return render(request, 'bugsocial/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = SignupForm()

    return render(request, 'bugsocial/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        # store data in the built in user object
        user_form = UserEditForm(instance=request.user, data=request.POST)
        # store profile data in the custom profile object
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # save profile and user details in database
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'bugsocial/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)

    return render(request, 'bugsocial/user/list.html',
                  {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    return render(request, 'bugsocial/user/detail.html',
                  {'section': 'people', 'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)

            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
