from django.urls import path
from admin_panel import views as admin_views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', admin_views.DashboardViewSet.as_view(), name='dashboard'),
    path('users_list/', admin_views.UsersListViewSet.as_view(), name='users_list'),
    path('user/', admin_views.UserViewSet.as_view(), name='user'),
    path('delete_user/', admin_views.delete_user, name='delete_user'),
    path('block_user/', admin_views.block_user, name='block_user'),

    path('trending_keywords/', admin_views.TrendingKeywordsViewSet.as_view(), name='trending_keywords'),
]