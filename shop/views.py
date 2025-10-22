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
