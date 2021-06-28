from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from customer.models import User
from django.views import View
from customer.serializers import UserSerializer
from django.utils.decorators import method_decorator
from customer.decorators import admin_login_required

# Create your views here.


@method_decorator(admin_login_required, name='dispatch')
class DashboardViewSet(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.filter().exclude(is_superuser=True).count()
        return context


@method_decorator(admin_login_required, name='dispatch')
class UsersListViewSet(TemplateView):
    template_name = 'users_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter().exclude(is_superuser=True)
        return context


@method_decorator(admin_login_required, name='dispatch')
class UserViewSet(View):

    def get(self, request):
        return render(request, 'users_create.html')

    def post(self, request):
        data = request.POST
        serializer = UserSerializer(data=data, many=False, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "User created")
            return redirect('admin_panel:users_list')
        elif serializer.errors:
            messages.warning(request, serializer.errors)
            return redirect('admin_panel:users_list')


@admin_login_required
def delete_user(request):
    if request.GET.get('user_id'):
        if User.objects.filter(id=request.GET.get('user_id')).exists():
            User.objects.filter(id=request.GET.get('user_id')).delete()
            messages.success(request, "User deleted!!!")
            return redirect('admin_panel:users_list')
        else:
            messages.warning(request, "User not found")
            return redirect('admin_panel:users_list')
    else:
        messages.warning(request, "User details required")
        return redirect('admin_panel:users_list')


@admin_login_required
def block_user(request):
    if request.GET.get('user_id'):
        if User.objects.filter(id=request.GET.get('user_id')).exists():
            user_obj = User.objects.get(id=request.GET.get('user_id'))
            if user_obj.is_active:
                user_obj.is_active = False
                messages.success(request, "User Blocked!!!")
            else:
                user_obj.is_active = True
                messages.success(request, "User Unblocked!!!")
            user_obj.save()
            return redirect('admin_panel:users_list')
        else:
            messages.warning(request, "User not found")
            return redirect('admin_panel:users_list')
    else:
        messages.warning(request, "User details required")
        return redirect('admin_panel:users_list')
