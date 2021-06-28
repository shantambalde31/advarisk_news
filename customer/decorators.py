from django.shortcuts import redirect
from django.contrib.auth import logout
from functools import wraps
from django.contrib import messages


def admin_login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return func(request, *args, **kwargs)
        elif request.user.is_authenticated and not request.user.is_superuser:
            logout(request)
            messages.warning(request, "You don't have access to admin panel")
            return redirect('customer:login')
        else:
            messages.warning(request, "You don't have access to admin panel")
            return redirect('customer:login')
    return wrap


def user_login_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.warning(request, "You don't have access to admin panel")
            return redirect('customer:login')
    return wrap
