from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from .auth_backend import PasswordlessAuthBackend
from django.shortcuts import render, redirect
from .models import CustomUser


def error_view(request):
    return render(request, 'error.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser(email=email, username=email)
            user.is_active = False
            user.set_unusable_password()
        user.send_magic_link()
        print('A magic link has been sent to your email address')
        return redirect('login_requested')
    else:
        return render(request, 'login.html')


def magic_link_view(request):
    token = request.GET.get('magic_token')
    print(token)
    try:
        user = CustomUser.objects.get(
            magic_token=token)
    except CustomUser.DoesNotExist:
        return redirect('userdne')
    else:
        user.magic_token = None
        user.magic_token_expires_at = None
        user.save()
        # Log user in
        # ...
        return redirect('')


def validate_magic_link(request):
    token = request.GET.get('magic_token')
    print('token', token)

    try:
        user = CustomUser.objects.get(magic_token=token)
    except CustomUser.DoesNotExist:
        print('The magic link is invalid or has expired.')
        return redirect('login')
    else:
        print('user.email', user.email, 'hello 98567289347')
        user.magic_token = None
        user.magic_token_expires_at = None
        user.is_active = True
        user.save()
        # Authenticate and log the user in
        auth_user = PasswordlessAuthBackend().authenticate(
            email=user.email)
        print(auth_user)
        login(request, auth_user)
        print('You have been logged in successfully.')
        return redirect('profile/')


def registration():
    pass


@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        # replace 'home' with the name of your homepage URL pattern
        return redirect('/')
    else:
        return render(request, 'delete_account.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('hello, form')
        if form.is_valid():
            print('form is valid')
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.set_unusable_password()
            user.send_magic_link()
            # user.save()
            return render(request, 'signup_success.html', )
        else:
            print('form is invalid')
            print(form.errors)
    else:
        print('hello else')
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout')
    return render(request, 'logout_success.html')


def login_requested_view(request):
    return render(request, 'login_requested.html')
