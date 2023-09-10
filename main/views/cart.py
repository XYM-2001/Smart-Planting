from django.shortcuts import render, get_object_or_404
from main.models import Product
from django.shortcuts import redirect
from main.models import Cart, CartItem
from authentication.models import User

def view_cart(request):
    user = request.user
    #user = get_object_or_404(User, pk=request.session['user_id'])
    cart, created = Cart.objects.get_or_create(user=user, ordered=False)

    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'cart': cart,
    })


def add_to_cart(request, slug):
    user = request.user
    #user = get_object_or_404(User, pk=request.session['user_id'])
    cart, created = Cart.objects.get_or_create(user=user, ordered=False)
    product = get_object_or_404(Product, pk=product_id)

    # 查看购物车中是否已存在该商品
    cart_item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        cart=cart,
    )

    if created:
        cart_item.price = product.price  # 如果是新创建的购物车项，设置价格
    else:
        cart_item.quantity += 1  # 如果购物车项已存在，增加数量
        cart_item.price += product.price  # 增加总价

    cart_item.save()

    # 更新购物车的总价
    cart.total_price += product.price
    cart.save()

    return redirect('main/cart.html')