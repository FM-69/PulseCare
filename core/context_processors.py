from .models import Cart, CartItem, MessageRequest

def cart_item_count(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == "PATIENT":
        try:
            cart = Cart.objects.get(patient=request.user)
            cart_item_count = cart.items.count()
        except Cart.DoesNotExist:
            cart_item_count = 0
    else:
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}

def accepted_message_requests(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'DOCTOR':
        accepted_requests = MessageRequest.objects.filter(
            doctor__user=request.user,
            status='ACCEPTED'
        ).select_related('patient')
        return {'accepted_message_requests': accepted_requests}
    return {'accepted_message_requests': []}