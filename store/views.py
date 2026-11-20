from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegistrationForm
from .models import Category, Order, OrderItem, Product


def get_cart(request):
    return request.session.setdefault('cart', {})


def cart_summary(request):
    cart = get_cart(request)
    items = []
    total = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if product:
            quantity = int(quantity)
            subtotal = product.price * quantity
            total += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    return items, total


def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(is_active=True, stock__gt=0)[:8]
    return render(request, 'home.html', {'categories': categories, 'featured_products': featured})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/product_detail.html', {'product': product})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created.')
            return redirect('account')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next') or 'account')
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def account(request):
    return render(request, 'accounts/account.html', {'recent_orders': request.user.orders.all()[:5]})


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', slug=get_object_or_404(Product, id=product_id).slug)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 0
    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1.')
    else:
        cart = get_cart(request)
        key = str(product_id)
        new_quantity = int(cart.get(key, 0)) + quantity
        if new_quantity > product.stock:
            messages.error(request, 'That quantity is not available.')
        else:
            cart[key] = new_quantity
            request.session.modified = True
            messages.success(request, f'{product.name} added to cart.')
    return redirect('cart')


def cart(request):
    items, total = cart_summary(request)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})


def update_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        key = str(product_id)
        action = request.POST.get('action')
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(cart.get(key, 0))
        if action == 'increase':
            quantity += 1
        elif action == 'decrease':
            quantity -= 1
        elif action == 'remove':
            quantity = 0
        if quantity > product.stock:
            messages.error(request, 'That quantity is not available.')
        elif quantity <= 0:
            cart.pop(key, None)
            request.session.modified = True
        else:
            cart[key] = quantity
            request.session.modified = True
    return redirect('cart')


@login_required
def checkout(request):
    items, total = cart_summary(request)
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    locked_products = {product.id: product for product in Product.objects.select_for_update().filter(id__in=[str(item['product'].id) for item in items])}
                    calculated_total = Decimal('0.00')
                    for item in items:
                        product = locked_products[item['product'].id]
                        quantity = item['quantity']
                        if not product.is_active or quantity > product.stock:
                            raise ValueError(f'{product.name} has insufficient stock.')
                        calculated_total += product.price * quantity
                    order = Order.objects.create(
                        user=request.user,
                        recipient_name=form.cleaned_data['recipient_name'],
                        phone=form.cleaned_data['phone'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        total_amount=calculated_total,
                        payment_method='COD',
                    )
                    for item in items:
                        product = locked_products[item['product'].id]
                        quantity = item['quantity']
                        subtotal = product.price * quantity
                        OrderItem.objects.create(order=order, product=product, product_name=product.name, quantity=quantity, unit_price=product.price, subtotal=subtotal)
                        product.stock -= quantity
                        product.save(update_fields=['stock'])
                    request.session['cart'] = {}
                    request.session.modified = True
                return redirect('order_success', order_number=order.order_number)
            except ValueError as error:
                messages.error(request, str(error))
    else:
        form = CheckoutForm(initial={'recipient_name': request.user.get_full_name() or request.user.username, 'phone': ''})
    return render(request, 'orders/checkout.html', {'form': form, 'items': items, 'total': total})


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/success.html', {'order': order})


@login_required
def my_orders(request):
    return render(request, 'orders/my_orders.html', {'orders': request.user.orders.all()})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
