from django.urls import path
from . import views

app_name = 'pay'

urlpatterns = [
    path('ui', views.index, name='index'),
    path('api/accounts', views.get_accounts, name='get_accounts'),
    path('api/accounts/types', views.get_account_types, name='get_account_types'),
    path('api/accounts/currencies', views.get_currencies, name='get_currencies'),
    path('api/accounts/open', views.open_account, name='open_account'),
    path('api/accounts/<str:account_number>/deposit', views.deposit, name='deposit'),
    path('api/accounts/<str:account_number>/transfer', views.transfer, name='transfer'),
]