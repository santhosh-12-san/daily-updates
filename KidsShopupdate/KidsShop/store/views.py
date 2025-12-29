from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Slider, Category, Order
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import OrderItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# --- VIEW 1: Home Page (Updated for Category Filtering) ---
def home(request, category_slug=None):
    sliders = None
    products = None

    if category_slug:
        
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        
    else:
       
        products = Product.objects.all()
        sliders = Slider.objects.all()
    
    return render(request, 'home.html', {'products': products, 'sliders': sliders})

def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
         
            products = Product.objects.order_by('-created').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            product_count = products.count()
            
    return render(request, 'home.html', {'products': products, 'product_count': product_count})
# --- VIEW 3: Add to Cart (Restricted to Logged-in Users) ---
@login_required(login_url='login')  # <--- THIS IS THE MAGIC LINE
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    
    return redirect('cart_detail')

    

def cart_detail(request):
    total = 0
    quantity = 0
    cart_items = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except:
        pass 
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'quantity': quantity})

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


# --- VIEW 7: Register (FIXED) ---
def register(request):
    from django.contrib.auth.forms import UserCreationForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    # FIX: Use 'register.html' instead of 'registration/register.html'
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total = sum(item.product.price * item.quantity for item in cart_items)
    except:
        return redirect('home')

    if request.method == 'POST':
        # 1. Create the Order (The Receipt Header)
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            phone=request.POST.get('phone'),
            total_price=total
        )
        order.save()

        # 2. SAVE ORDER ITEMS (The Receipt List) <--- NEW PART
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # 3. Clear Cart & Finish
        cart_items.delete()
        return render(request, 'payment_success.html')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

# --- VIEW 10: Product Detail (Single Product Page) ---
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# --- VIEW 11: Edit Profile ---
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')
    return render(request, 'edit_profile.html')

# --- VIEW 12: My Orders List ---
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})
# --- VIEW 13: Order Detail (The Receipt) ---
# --- VIEW 13: Order Detail (Updated to prevent errors) ---
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Fetch the items belonging to this order
    order_items = OrderItem.objects.filter(order=order) 
    
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})