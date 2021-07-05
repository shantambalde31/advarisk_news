from django.shortcuts import redirect, render
from django.contrib.auth import logout
from functools import wraps
from django.contrib import messages
from datetime import datetime, timedelta
from customer.models import SearchedKeywords


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


def search_threshold(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        threshold_time = datetime.now() - timedelta(minutes=15)
        search_string = request.GET.get('search')
        if not SearchedKeywords.objects.filter(searched_by=request.user, keyword=search_string, last_search__gte=threshold_time):
            return func(request, *args, **kwargs)
        elif request.session.get(search_string):
            context = {
                'keyword': search_string,
                'articles': request.session.get(search_string)
            }
            messages.success(request, "Showing Last searched result for: " + search_string)
            return render(request, 'home.html', context)
        messages.warning(request, "You can't search the keyword frequently.")
        return redirect('customer:home')
    return wrap
