from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product

def landing(request):
    # Get all products
    products = Product.objects.all()
    
    # Get unique categories that actually have products - simplified approach

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
    related_products = Product.objects.filter(category=product.category)
    
    # Build breadcrumb trail
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': product.get_category_display_name(), 'url': f'/?categories={product.category}'},
        {'name': product.name, 'url': None}
    ]
    
    context = {
        'product': product,
        'related_products': related_products,
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/pdp.html', context)

def sign_in(request):
    return render(request, 'shop/sign-in.html')

def sign_up(request):
    return render(request, 'shop/sign-up.html')
