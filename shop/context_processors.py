from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        count = cart.get_total_items() if cart else 0
        return {'cart_count': count}
    return {'cart_count': 0}