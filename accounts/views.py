from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


def user_login(request):

    form = LoginForm()

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.role == 'manager':
                return redirect('manager_dashboard')

            elif user.role == 'tl':
                return redirect('tl_dashboard')

            else:
                return redirect('member_dashboard')

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


def user_logout(request):

    logout(request)

    return redirect('login')


def manager_dashboard(request):

    return render(
        request,
        'accounts/manager_dashboard.html'
    )


def tl_dashboard(request):

    return render(
        request,
        'accounts/tl_dashboard.html'
    )


def member_dashboard(request):

    return render(
        request,
        'accounts/member_dashboard.html'
    )