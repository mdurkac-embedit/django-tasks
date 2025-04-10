from django.urls import path
from . import views

app_name = 'pay'

urlpatterns = [
    path('ui', views.index, name='index'),
    path('api/accounts', views.get_accounts, name='get_accounts'),
    path('api/accounts/open', views.open_account, name='open_account'),
]