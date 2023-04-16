from django.urls import path
from . import views

app_name = 'database'

urlpatterns = [
    path('', views.database_view, name = 'database'),
    path('<int:beer_id>/', views.dynamic_info_view, name = 'send_info_dynamic'),
]