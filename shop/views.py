from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Product, UserProfile, Address, Cart, CartItem, Order, OrderItem, Feedback

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

def shop_products_api(request):
    """API endpoint to get filtered products without page refresh"""
    from decimal import Decimal, InvalidOperation
    
    # Get all active products
    products = Product.objects.filter(is_active=True)
    
    # Handle search - only search by name (title) and price
    search_query = request.GET.get('search', '')
    if search_query:
        # Search by name or price (convert price to string for partial matching)
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(price__startswith=search_query)
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
    
    # Serialize products to JSON
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'image_url': product.image_url,
            'category': product.category,
            'category_display': product.get_category_display_name(),
            'stock_quantity': product.stock_quantity,
            'stock_status': product.stock_status,
            'is_active': product.is_active,
            'is_in_stock': product.is_in_stock,
            'url': product.get_absolute_url(),
        })
    
    return JsonResponse({
        'products': products_data,
        'count': len(products_data)
    })
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

    # Redirect authenticated users to the home page
    if request.user.is_authenticated:
        return redirect('landing')
    
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

    # Redirect authenticated users to the home page
    if request.user.is_authenticated:
        return redirect('landing')
    
    # Breadcrumb for sign-up page
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Sign Up', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/sign-up.html', context)

def cart_count_api(request):
    """API endpoint to get current cart count"""
    cart = _get_or_create_cart(request)
    items = cart.items.all() if cart else []
    cart_item_count = sum(item.quantity for item in items)
    
    return JsonResponse({'count': cart_item_count})


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
    items = cart.items.select_related('product').all() if cart else []
    shipping_fee = Decimal('0.00')  # Placeholder; will be calculated in POST

    if request.method == "POST":
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, email, address, payment_method]):
            messages.error(request, "All fields are required.")
            return render(request, "shop/checkout.html", {
                "cart": cart,
                "items": items,
                "shipping_fee": shipping_fee
            })
        
        # Calculate subtotal
        subtotal = cart.total_price() if cart else Decimal('0.00')

        # Calculate shipping fee
        if subtotal < Decimal('200.00'):
            shipping_fee = Decimal('50.00')
        elif subtotal >= Decimal('200.00'):  # Adjusted to >= 300 as per your earlier request
            shipping_fee = Decimal('70.00')
        else:
            shipping_fee = Decimal('50.00')  # For 200-299
        
        total_amount = subtotal + shipping_fee

        with transaction.atomic():
            # Create Order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                address=address,
                payment_method=payment_method,
                total_amount=total_amount,
                shipping_fee=shipping_fee,
            )

            # Create OrderItems
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    #total_price=item.total_price(),
                )

            # Clear the cart
            cart.items.all().delete()

        # Show success page
        return render(request, "shop/checkout_success.html", {"order": order})

    return render(request, "shop/checkout.html", {
        "cart": cart,
        "items": items,
        "shipping_fee": shipping_fee
    })

@login_required
def user_profile(request):  # Renamed from 'profile' to 'user_profile'
    """User profile page"""
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Profile', 'url': None}
    ]
    
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
        except Exception:
            user_profile = None

        # Handle POST for editing profile information including profile picture
        if request.method == 'POST' and user_profile:
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                # Delete old profile picture if it exists
                if user_profile.profile_picture:
                    try:
                        user_profile.profile_picture.delete(save=False)
                    except Exception:
                        pass  # Ignore errors if file doesn't exist
                
                user_profile.profile_picture = request.FILES['profile_picture']
            
            # Handle personal information updates
            if 'update_personal_info' in request.POST:
                # Update User model fields
                first_name = request.POST.get('first_name', '').strip()
                last_name = request.POST.get('last_name', '').strip()
                email = request.POST.get('email', '').strip()
                
                if first_name:
                    request.user.first_name = first_name
                if last_name:
                    request.user.last_name = last_name
                if email:
                    request.user.email = email
                
                request.user.save()
                
                # Update UserProfile fields
                contact_number = request.POST.get('contact_number', '').strip()
                if contact_number:
                    user_profile.contact_number = contact_number
            
            # Handle settings updates
            if 'update_settings' in request.POST:
                preferred_currency = request.POST.get('preferred_currency', '')
                preferred_payment_method = request.POST.get('preferred_payment_method', '')
                
                if preferred_currency:
                    user_profile.preferred_currency = preferred_currency
                if preferred_payment_method:
                    user_profile.preferred_payment_method = preferred_payment_method
            
            # Handle address updates (legacy support)
            address = request.POST.get('house_address', '').strip()
            if address:
                user_profile.house_address = address
            
            user_profile.save()
    
    # Get user addresses
    user_addresses = []
    if request.user.is_authenticated:
        user_addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    context = {
        'breadcrumb_items': breadcrumb_items,
        'user': request.user,
        'user_profile': user_profile,
        'user_addresses': user_addresses,
    }

    return render(request, 'shop/profile.html', context)


def add_address(request):
    """Add a new address"""
    if not request.user.is_authenticated:
        return redirect('sign_in')
    
    if request.method == 'POST':
        try:
            # Get form data
            label = request.POST.get('label', '').strip()
            address_type = request.POST.get('address_type', 'home')
            street_address = request.POST.get('street_address', '').strip()
            city = request.POST.get('city', '').strip()
            state_province = request.POST.get('state_province', '').strip()
            postal_code = request.POST.get('postal_code', '').strip()
            country = request.POST.get('country', 'Philippines').strip()
            is_default = request.POST.get('is_default') == 'on'
            
            # Validate required fields
            if not all([label, street_address, city, state_province, postal_code]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('profile')
            
            # Create new address
            Address.objects.create(
                user=request.user,
                label=label,
                address_type=address_type,
                street_address=street_address,
                city=city,
                state_province=state_province,
                postal_code=postal_code,
                country=country,
                is_default=is_default
            )
            
            messages.success(request, 'Address added successfully!')
            
        except Exception as e:
            messages.error(request, f'Error adding address: {str(e)}')
    
    return redirect('profile')

def edit_address(request, address_id):
    """Edit an existing address"""
    if not request.user.is_authenticated:
        return redirect('sign_in')
    
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Update address fields
            address.label = request.POST.get('label', '').strip()
            address.address_type = request.POST.get('address_type', 'home')
            address.street_address = request.POST.get('street_address', '').strip()
            address.city = request.POST.get('city', '').strip()
            address.state_province = request.POST.get('state_province', '').strip()
            address.postal_code = request.POST.get('postal_code', '').strip()
            address.country = request.POST.get('country', 'Philippines').strip()
            address.is_default = request.POST.get('is_default') == 'on'
            
            # Validate required fields
            if not all([address.label, address.street_address, address.city, address.state_province, address.postal_code]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('profile')
            
            address.save()
            messages.success(request, 'Address updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating address: {str(e)}')
    
    return redirect('profile')

def delete_address(request, address_id):
    """Delete an address"""
    if not request.user.is_authenticated:
        return redirect('sign_in')
    
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        try:
            address.delete()
            messages.success(request, 'Address deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting address: {str(e)}')
    
    return redirect('profile')

def change_password(request):
    """Change user password"""
    if not request.user.is_authenticated:
        return redirect('sign_in')
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('profile')
        
        # Validate new password
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('profile')
        
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('profile')
        
        try:
            # Change password
            request.user.set_password(new_password)
            request.user.save()
            
            # Update session to prevent logout
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Password changed successfully!')
        except Exception as e:
            messages.error(request, f'Error changing password: {str(e)}')
    
    return redirect('profile')

def delete_account(request):
    """Delete user account with confirmation"""
    if not request.user.is_authenticated:
        return redirect('sign_in')
    
    if request.method == 'POST':
        password_confirmation = request.POST.get('password_confirmation')
        
        # Verify password
        if not request.user.check_password(password_confirmation):
            messages.error(request, 'Incorrect password. Account deletion cancelled.')
            return redirect('profile')
        
        try:
            # Delete user's related data first
            user = request.user
            
            # Delete user's addresses
            Address.objects.filter(user=user).delete()
            
            # Delete user profile if exists
            try:
                if hasattr(user, 'userprofile'):
                    user.userprofile.delete()
            except:
                pass  # Profile might not exist
            
            # Store username for farewell message
            username = user.username
            
            # Delete the user account
            user.delete()
            
            # Clear session
            request.session.flush()
            
            # Redirect to landing page with message
            messages.success(request, f'Account for {username} has been permanently deleted. We\'re sorry to see you go!')
            return redirect('landing')
            
        except Exception as e:
            messages.error(request, f'Error deleting account: {str(e)}')
            return redirect('profile')
    
    return redirect('profile')

def feedback(request):
    """Feedback page"""
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Feedback', 'url': None}
    ]
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            category = request.POST.get('category', 'general')
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Validate required fields
            if not all([name, email, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('feedback')
            
            # Create feedback
            feedback_obj = Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                category=category,
                subject=subject,
                message=message
            )
            
            messages.success(request, 'Thank you for your feedback! We will review it shortly.')
            return redirect('feedback')
            
        except Exception as e:
            messages.error(request, f'Error submitting feedback: {str(e)}')
            return redirect('feedback')
    
    # Get category choices for the form
    category_choices = Feedback.CATEGORY_CHOICES
    
    # Pre-fill user data if authenticated
    initial_data = {}
    if request.user.is_authenticated:
        initial_data['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        initial_data['email'] = request.user.email
    
    context = {
        'breadcrumb_items': breadcrumb_items,
        'category_choices': category_choices,
        'initial_data': initial_data,
    }
    
    return render(request, 'shop/feedback.html', context)

def feedback_success(request):
    """Feedback success page"""
    breadcrumb_items = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Feedback', 'url': '/feedback/'},
        {'name': 'Success', 'url': None}
    ]
    
    context = {
        'breadcrumb_items': breadcrumb_items,
    }
    
    return render(request, 'shop/feedback_success.html', context)
