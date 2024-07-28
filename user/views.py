# auth/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Cart, CartProduct
from .forms import SignUpForm, LoginForm
from products.models import product
from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product_instance = product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product_instance)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return JsonResponse({'success': True})

@login_required
def remove_from_cart(request, product_id):
    product_instance = product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_product = CartProduct.objects.get(cart=cart, product=product_instance)
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    else:
        cart_product.delete()
    return redirect('cart:cart')

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after signup
            login(request, user)
            return redirect('products')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('cart:login')
