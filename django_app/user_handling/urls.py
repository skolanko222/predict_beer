from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('', views.login_fun, name='login'),
    path('registration/', views.register, name='registration'),
    path('logout/', views.logout_fun, name='logout'),
    path('history/', views.history, name="history")
]