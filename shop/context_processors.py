from .models import Cart

def cart_context(request):
    """Add cart information to all template contexts"""
    cart_item_count = 0
    
    if hasattr(request, 'user'):
        try:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            if request.user.is_authenticated:
                cart = Cart.objects.filter(user=request.user, is_active=True).first()
            else:
                cart = Cart.objects.filter(session_key=session_key, user=None, is_active=True).first()
            
            if cart:
                cart_item_count = sum(item.quantity for item in cart.items.all())
                
        except Exception:
            cart_item_count = 0
    
    return {
        'cart_item_count': cart_item_count
    }