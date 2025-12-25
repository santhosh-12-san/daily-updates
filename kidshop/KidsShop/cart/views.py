from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def cart_detail(request):
    return render(request, 'cart/cart.html')


@login_required
def add_to_cart(request):
    # Temporary logic (we will improve later)
    return redirect('cart:cart_detail')
