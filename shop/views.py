from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, Quantity, Type, ProductImage
import json


def index(request):
    products = Product.objects.filter(in_stock=True)[:6]
    categories = Category.objects.filter(parent__isnull=True)
    reviews = Review.objects.filter(is_approved=True)[:3]
    context = {
        'products': products,
        'categories': categories,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent__isnull=True)
    quantities = Quantity.objects.all()
    types = Type.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    selected_quantities = request.GET.getlist('quantity')
    selected_types = request.GET.getlist('product_type')
    sort_by = request.GET.get('sort')

    if category_slug and category_slug.strip():
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query and search_query.strip():
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if selected_quantities:
        products = products.filter(quantity_id__in=selected_quantities)

    if selected_types:
        products = products.filter(product_type_id__in=selected_types)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'quantities': quantities,
        'types': types,
        'current_category': category_slug,
        'search_query': search_query,
        'selected_quantities': selected_quantities,
        'selected_types': selected_types,
        'sort_by': sort_by,
    }
    return render(request, 'catalog.html', context)


def about(request):
    return render(request, 'about.html')


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    reviews = Review.objects.filter(product=product, is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'product_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.user.is_admin_user():
        messages.error(request, 'Администратор не может оформлять заказы')
        return redirect('catalog')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

    quantity = int(request.POST.get('quantity', 1))
    chocolate_type = request.POST.get('chocolate_type', '')
    chocolate_color = request.POST.get('chocolate_color', '')
    packaging_type = request.POST.get('packaging_type', '')
    packaging_color = request.POST.get('packaging_color', '')
    extra_berries = request.POST.get('extra_berries', '')
    flower_type = request.POST.get('flower_type', '')
    flower_color = request.POST.get('flower_color', '')

    # Рассчитываем доплату
    extra_price = 0
    if chocolate_type == 'colored':
        extra_price += 150
    if packaging_type == 'satin':
        extra_price += 350
    elif packaging_type == 'matte':
        extra_price += 600
    if packaging_color == 'gold' or packaging_color == 'silver':
        extra_price += 100
    if extra_berries:
        extra_price += 650
    if flower_type == 'rose':
        extra_price += 700
    elif flower_type == 'eustoma':
        extra_price += 850
    elif flower_type == 'gypsophila':
        extra_price += 300
    elif flower_type == 'chrysanthemum':
        extra_price += 400
    elif flower_type == 'peony':
        extra_price += 900

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            'quantity': quantity,
            'chocolate_type': chocolate_type,
            'chocolate_color': chocolate_color,
            'packaging_type': packaging_type,
            'packaging_color': packaging_color,
            'extra_berries': extra_berries,
            'flower_type': flower_type,
            'flower_color': flower_color,
            'extra_price': extra_price
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.chocolate_type = chocolate_type
        cart_item.chocolate_color = chocolate_color
        cart_item.packaging_type = packaging_type
        cart_item.packaging_color = packaging_color
        cart_item.extra_berries = extra_berries
        cart_item.flower_type = flower_type
        cart_item.flower_color = flower_color
        cart_item.extra_price = extra_price
        cart_item.save()

    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('cart')


@login_required
def cart(request):
    if request.user.is_admin_user():
        messages.error(request, 'Администратор не может оформлять заказы')
        return redirect('admin_dashboard')

    cart = Cart.objects.filter(user=request.user, is_active=True).first()
    return render(request, 'cart.html', {'cart': cart})


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        elif quantity == 0:
            cart_item.delete()

        return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    if request.user.is_admin_user():
        messages.error(request, 'Администратор не может оформлять заказы')
        return redirect('admin_dashboard')

    cart = Cart.objects.filter(user=request.user, is_active=True).first()

    if not cart or cart.items.count() == 0:
        messages.error(request, 'Корзина пуста')
        return redirect('cart')

    if request.method == 'POST':
        address = f"{request.POST.get('city', '')}, {request.POST.get('address', '')}"

        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            delivery_address=address,
            phone=request.POST.get('phone'),
            comment=request.POST.get('comment', ''),
            delivery_date=request.POST.get('delivery_date'),
            delivery_time=request.POST.get('delivery_time')
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                chocolate_type=cart_item.chocolate_type,
                chocolate_color=cart_item.chocolate_color,
                packaging_type=cart_item.packaging_type,
                packaging_color=cart_item.packaging_color,
                extra_berries=cart_item.extra_berries,
                flower_type=cart_item.flower_type,
                flower_color=cart_item.flower_color,
                extra_price=cart_item.extra_price
            )

        cart.is_active = False
        cart.save()

        messages.success(request, f'Заказ #{order.id} успешно оформлен')
        return redirect('profile')

    return render(request, 'checkout.html', {'cart': cart})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': orders})


def reviews(request):
    if request.method == 'POST' and request.user.is_authenticated and not request.user.is_admin_user():
        product_id = request.POST.get('product_id')
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        image = request.FILES.get('image')

        product = get_object_or_404(Product, id=product_id)

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment,
            image=image
        )

        messages.success(request, 'Отзыв добавлен и будет проверен')
        return redirect('reviews')

    reviews_list = Review.objects.filter(is_approved=True).order_by('-created_at')
    products = Product.objects.all()
    avg_rating = reviews_list.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'reviews.html', {
        'reviews': reviews_list,
        'products': products,
        'avg_rating': avg_rating
    })


def get_cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        count = cart.get_total_items() if cart else 0
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items = []
    for item in order.items.all():
        items.append({
            'name': item.product.name,
            'quantity': item.quantity,
            'price': str(item.price),
            'total': str(item.get_total_price()),
        })

    data = {
        'status': order.get_status_display(),
        'status_class': order.status,
        'date': order.created_at.strftime('%d.%m.%Y %H:%M'),
        'items': items,
        'address': order.delivery_address,
        'phone': order.phone,
        'comment': order.comment,
        'total': str(order.total_price),
    }

    return JsonResponse(data)