from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import login, logout
from advarisk_news.backends.backends import AuthBackend
from django.utils.decorators import method_decorator
from customer.decorators import user_login_required, search_threshold
from django.conf import settings
import requests
from customer.models import SearchedKeywords
from datetime import datetime
from customer.services import SearchNewsService
# Create your views here.


class LoginViewSet(View):

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('admin_panel:dashboard')
        elif request.user.is_authenticated and not request.user.is_superuser:
            return redirect('customer:home')
        else:
            return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = AuthBackend.authenticate(self, email=email, password=password)
            if user:
                if user and user.is_superuser:
                    login(request, user)
                    return redirect('admin_panel:dashboard')
                elif user and user.is_active:
                    login(request, user)
                    return redirect('customer:home')
                elif user and not user.is_active:
                    messages.warning(request, "You are currently blocked")
                    return redirect('customer:login')
                else:
                    messages.warning(request, "You don't have access to admin panel")
                    return redirect('customer:login')
            else:
                messages.warning(request, 'Email or Password Incorrect.')
                return render(request, 'login.html')
        else:
            messages.warning(request, 'Please provide email and Password')
            return render(request, 'login.html')


class LogoutViewSet(View):

    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logged out!!!")
        return redirect('customer:login')


@method_decorator(user_login_required, name='dispatch')
class HomePageViewSet(TemplateView):
    template_name = "home.html"


@method_decorator(user_login_required, name='dispatch')
@method_decorator(search_threshold, name='dispatch')
class SearchNewsViewSet(View):

    def get(self, request):

        data = request.GET
        search_string = data.get('search').strip()
        if search_string:
            searched_keyword, created = SearchedKeywords.objects.get_or_create(keyword=search_string,
                                                                               searched_by=request.user)
            searched_keyword.last_search = datetime.now()
            searched_keyword.save()
            result = SearchNewsService.get_news(search_string)
            if result.get('status') == 'ok':
                articles = result.get('articles')
                if articles:
                    context = {
                        'keyword': search_string,
                        'articles': articles
                    }
                    messages.success(request, "Searched results for : " + str(data.get('search')))
                    request.session[search_string] = articles
                    return render(request, 'home.html', context)
                else:
                    messages.warning(request, "No articles found for this keyword!!!")
                    return redirect("customer:home")
            else:
                messages.warning(request, "Something went wrong!!!")
                return redirect("customer:home")
        else:
            messages.warning(request, "Please provide search string")
            return redirect("customer:home")


@method_decorator(user_login_required, name='dispatch')
@method_decorator(search_threshold, name='dispatch')
class RefreshSearchNewsViewSet(View):

    def get(self, request):
        data = request.GET
        search_string = data.get('search').strip()
        if search_string:
            searched_keyword, created = SearchedKeywords.objects.get_or_create(keyword=search_string,
                                                                               searched_by=request.user)
            searched_keyword.last_search = datetime.now()
            searched_keyword.save()
            result = SearchNewsService.refresh_news(search_string)
            if result.get('status') == 'ok':
                articles = result.get('articles')
                if articles:
                    context = {
                        'keyword': search_string,
                        'articles': articles
                    }
                    messages.success(request, "Refreshed results for : " + str(data.get('search')))
                    request.session[search_string] = articles
                    return render(request, 'home.html', context)
                else:
                    messages.warning(request, "No articles found for this keyword!!!")
                    return redirect("customer:home")
            else:
                messages.warning(request, "Something went wrong!!!")
                return redirect("customer:home")
        else:
            messages.warning(request, "Please provide search string")
            return redirect("customer:home")
