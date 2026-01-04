from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem, Slider, Category, Order
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import OrderItem
from .models import AddressBook

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def home(request, category_slug=None):
    
    categories = Category.objects.all() 
    sliders = Slider.objects.all()      
    if category_slug:
        sliders =None
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
       
        products = Product.objects.all()

    sort_by = request.GET.get('sort')
    
    if sort_by == 'low-to-high':
        products = products.order_by('price')
    elif sort_by == 'high-to-low':
        products = products.order_by('-price')
    elif sort_by == 'alphabetic':
        products = products.order_by('name')

    context = {
        'products': products,
        'sliders': sliders,
        'categories': categories, 
    }
    return render(request, 'home.html', context)

def search(request):
    
    products = None
    product_count = 0
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            
            sort_by = request.GET.get('sort')
            if sort_by == 'low-to-high':
                products = products.order_by('price')
            elif sort_by == 'high-to-low':
                products = products.order_by('-price')
            elif sort_by == 'alphabetic':
                products = products.order_by('name')
                
            product_count = products.count()

    return render(request, 'home.html', {'products': products, 'product_count': product_count})

@login_required(login_url='login')  
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

    if request.GET.get('action') == 'buy_now':
        return redirect('checkout')  
    return redirect(request.META.get('HTTP_REFERER', 'home'))


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

def register(request):
    from django.contrib.auth.forms import UserCreationForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

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
    saved_addresses = AddressBook.objects.filter(user=request.user)

    if request.method == 'POST':
        try:
            order = Order.objects.create(
                user=request.user,
                full_name=request.POST.get('full_name'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),  
                total_price=total
            )
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart_items.delete()
            
            return render(request, 'payment_success.html')
            
        except Exception as e:
            print(f"Error saving order: {e}") 
            return redirect('checkout')
    context = {
        'cart_items': cart_items,
        'total': total,
        'saved_addresses': saved_addresses,
    }
    return render(request, 'checkout.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


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

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order) 
    
    
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order) 
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'categories_list.html', {'categories': categories})

@login_required
def my_addresses(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    unique_addresses = []
    seen = set()
    for order in orders:
        identifier = f"{order.address}-{order.city}"
        if identifier not in seen:
            unique_addresses.append(order)
            seen.add(identifier)
    return render(request, 'my_addresses.html', {'addresses': unique_addresses})


@login_required
def my_addresses(request):
    addresses = AddressBook.objects.filter(user=request.user)
    return render(request, 'my_addresses.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line = request.POST.get('address_line')
        city = request.POST.get('city')
        state = request.POST.get('state')
    
        address = AddressBook(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line=address_line,
            city=city,
            state=state
        )
        address.save()
        
        return redirect('my_addresses')
    return render(request, 'add_address.html')