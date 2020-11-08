from django.urls import path
from . import views

app_name = 'FinalApp'

urlpatterns = [
    path('', views.main, name="main"),
    path('place_list/', views.place_list, name='place_list'),
    path('place_detail/', views.place_detail, name='place_detail'),
    path('place_route/', views.place_route, name='place_route'),


]