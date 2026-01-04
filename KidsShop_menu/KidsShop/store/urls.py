from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('categories/', views.categories_list, name='categories_list'),
    path('my_addresses/', views.my_addresses, name='my_addresses'),
    path('my_addresses/', views.my_addresses, name='my_addresses'),
    path('add_address/', views.add_address, name='add_address'),
]