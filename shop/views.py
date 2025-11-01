from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product

def landing(request):
    """Homepage with featured products, bestsellers, and new arrivals"""
    
    # Get featured products (limit to 8)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    
    # Get bestsellers (limit to 8)
    bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:8]
    
    # Get new arrivals (products from last 30 days, limit to 8)
    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_arrivals = Product.objects.filter(
        is_active=True, 
        created_at__gte=thirty_days_ago
    ).order_by('-created_at')[:8]
    
    # Breadcrumb for homepage (just "Home")
    breadcrumb_items = [
        {'name': 'Home', 'url': None}
    ]
    
    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/landing.html', context)

def shop(request):
    """Shop page with all products and filtering"""
    # Get all active products
    products = Product.objects.filter(is_active=True)
    
    # Get unique categories that actually have products
    existing_categories = set(Product.objects.exclude(category='').values_list('category', flat=True))
    category_choices = [
        (cat, dict(Product.CATEGORIES_CHOICES).get(cat, cat)) 
        for cat in existing_categories
    ]
    # Sort alphabetically by display name
    category_choices.sort(key=lambda x: (x[1] or '').lower())
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Handle category filtering
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        products = products.filter(category__in=selected_categories)
    
    # Handle sorting
    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'a-to-z':
        products = products.order_by('name')
    elif sort_by == 'z-to-a':
        products = products.order_by('-name')
    elif sort_by == 'price-lowest-first':
        products = products.order_by('price')
    elif sort_by == 'price-highest-first':
        products = products.order_by('-price')
    elif sort_by == 'recently-added':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Build breadcrumb trail for shop page
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Shop', 'url': None}
    ]
    
    context = {
        'products': products,
        'category_choices': category_choices,
        'search_query': search_query,
        'selected_categories': selected_categories,
        'sort_by': sort_by,
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/shop.html', context)

def pdp(request, slug):
    """View for individual product details"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(slug=slug)[:4]
    
    # Build breadcrumb trail
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Shop', 'url': '/shop/'},
        {'name': product.get_category_display_name(), 'url': f'/shop/?categories={product.category}'},
        {'name': product.name, 'url': None}
    ]
    
    context = {
        'product': product,
        'related_products': related_products,
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/pdp.html', context)

def sign_in(request):
    # Breadcrumb for sign-in page
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Sign In', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/sign-in.html', context)

def sign_up(request):
    # Breadcrumb for sign-up page
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Sign Up', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/sign-up.html', context)

def cart(request):

    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'My Cart', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }

    return render(request, 'shop/cart.html', context)


def about_us(request):
    """About Us page rendering a prototype-style layout"""
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'About us', 'url': None}
    ]

    context = {
        'breadcrumb_items': breadcrumb_items,
    }

    return render(request, 'shop/about-us.html', context)


def contact_us(request):
    """Contact Us page"""
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Contact us', 'url': None}
    ]

    context = {
        'breadcrumb_items': breadcrumb_items,
    }

    return render(request, 'shop/contact-us.html', context)

from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Product, Cart, CartItem

# ...existing code...
def cart(request):

    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'My Cart', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }

    return render(request, 'shop/cart.html', context)

def _get_or_create_cart(request):
    """Return an active Cart for the current user or session."""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True, defaults={'session_key': session_key})
        # If there is an anonymous cart for this session, merge it
        try:
            anon_cart = Cart.objects.get(session_key=session_key, user__isnull=True, is_active=True)
            if anon_cart.pk != cart.pk:
                with transaction.atomic():
                    for item in anon_cart.items.all():
                        ci, created = CartItem.objects.get_or_create(
                            cart=cart,
                            product=item.product,
                            defaults={'quantity': item.quantity, 'price': item.price}
                        )
                        if not created:
                            ci.quantity += item.quantity
                            ci.save()
                    anon_cart.is_active = False
                    anon_cart.save()
        except Cart.DoesNotExist:
            pass
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key, user=None, is_active=True)
    return cart

@require_POST
def add_to_cart(request):
    """Add product to cart or increment quantity."""
    product_id = request.POST.get('product_id')
    qty = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, pk=product_id)

    cart = _get_or_create_cart(request)
    with transaction.atomic():
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': qty, 'price': product.price}
        )
        if not created:
            item.quantity += qty
            item.save()
    # redirect to the same URL that serves your cart page
    return redirect('cart')
    
def cart_detail(request):
    """Show cart and line items (alias of cart view)."""
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    return render(request, 'shop/cart.html', {'cart': cart, 'items': items})

# Replace the simple cart view above with this one so /cart/ shows items
def cart(request):
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'My Cart', 'url': None}
    ]
    cart_obj = _get_or_create_cart(request)
    items = cart_obj.items.select_related('product').all() if cart_obj else []
    context = {
        'breadcrumb_items': breadcrumb_items,
        'cart': cart_obj,
        'items': items,
    }
    return render(request, 'shop/cart.html', context)

@require_POST
def update_cart_item(request, item_id):
    """Update quantity for a given cart item (set or remove if 0)."""
    qty = int(request.POST.get('quantity', 0))
    item = get_object_or_404(CartItem, pk=item_id)
    # Ensure item belongs to the current cart
    cart = _get_or_create_cart(request)
    if item.cart_id != cart.id:
        return redirect('cart_detail')
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart_detail')

@require_POST
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    cart = _get_or_create_cart(request)
    if item.cart_id == cart.id:
        item.delete()
    return redirect('cart_detail')

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

def checkout(request):
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    shipping_fee = 0  # Set your shipping fee logic if needed

    if request.method == "POST":
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'COD')
        total_amount = cart.total_price + shipping_fee

        # Create Order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            address=address,
            payment_method=payment_method,
            total_amount=total_amount,
            status='Pending'
        )

        # Create OrderItems
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )

        # Optionally clear the cart
        cart.items.all().delete()
        cart.is_active = False
        cart.save()

        # Show success page
        return render(request, "shop/checkout_success.html", {"order": order})

    return render(request, "shop/checkout.html", {"cart": cart, "items": items, "shipping_fee": shipping_fee})