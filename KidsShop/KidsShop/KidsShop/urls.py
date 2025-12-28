from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    

    path('', store_views.home, name='home'),
    path('search/', store_views.search, name='search'),
    path('add_to_cart/<int:product_id>/', store_views.add_to_cart, name='add_to_cart'),
    path('cart/', store_views.cart_detail, name='cart_detail'),
    path('remove_cart/<int:product_id>/', store_views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', store_views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', store_views.checkout, name='checkout'),
    path('profile/', store_views.profile, name='profile'),
    
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/register/', store_views.register, name='register'),
    path('category/<slug:category_slug>/', store_views.home, name='products_by_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)