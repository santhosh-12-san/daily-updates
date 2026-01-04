from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.home, name='home'),
    path('category/<slug:category_slug>/', store_views.home, name='products_by_category'),
    path('search/', store_views.search, name='search'),
    path('product/<int:product_id>/', store_views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', store_views.add_to_cart, name='add_to_cart'),
    path('cart/', store_views.cart_detail, name='cart_detail'),
    path('remove_cart/<int:product_id>/', store_views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', store_views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', store_views.checkout, name='checkout'),
    path('profile/', store_views.profile, name='profile'),
    path('profile/edit/', store_views.edit_profile, name='edit_profile'),
    path('orders/', store_views.my_orders, name='my_orders'),
    path('orders/view/<int:order_id>/', store_views.order_detail, name='order_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/register/', store_views.register, name='register'),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)