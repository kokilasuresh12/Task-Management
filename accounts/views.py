from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm


def user_login(request):

    form = LoginForm()
    error = ""

    if request.method == "POST":

        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            if user.role != role:
                error = "Selected role does not match user role."

            else:
                login(request, user)

                if role == 'manager':
                    return redirect('manager_dashboard')

                elif role == 'tl':
                    return redirect('tl_dashboard')

                elif role == 'member':
                    return redirect('member_dashboard')

        else:
            error = "Invalid username or password."

    return render(
        request,
        'accounts/login.html',
        {
            'form': form,
            'error': error
        }
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