from django.urls import path
from customer import views as customer_views

app_name = 'customer'

urlpatterns = [
    path('', customer_views.LoginViewSet.as_view(), name='login'),
    path('logout', customer_views.LogoutViewSet.as_view(), name='logout'),
    path('home/', customer_views.HomePageViewSet.as_view(), name='home'),
    path('search_news/', customer_views.SearchNewsViewSet.as_view(), name='search_news'),
    path('refresh_search_news/', customer_views.RefreshSearchNewsViewSet.as_view(), name='refresh_search_news'),
]
