from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product, Order, Quantity, Type, ProductImage


@staff_member_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        return redirect('index')

    products = Product.objects.all().order_by('-created_at')
    quantities = Quantity.objects.all()
    types = Type.objects.all()

    active_tab = request.GET.get('tab', 'products')

    if request.method == 'POST':
        if 'update_stock' in request.POST:
            product_id = request.POST.get('product_id')
            in_stock = request.POST.get('in_stock') == 'on'
            product = get_object_or_404(Product, id=product_id)
            product.in_stock = in_stock
            product.save()
            messages.success(request, f'Наличие обновлено для {product.name}')
            return redirect(f'/admin-panel/?tab=products')

        elif 'add_product' in request.POST:
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = float(request.POST.get('price'))
            type_id = request.POST.get('product_type')
            quantity_id = request.POST.get('quantity')
            in_stock = request.POST.get('in_stock') == 'on'
            images = request.FILES.getlist('images')

            product_type = get_object_or_404(Type, id=type_id) if type_id else None
            quantity = get_object_or_404(Quantity, id=quantity_id) if quantity_id else None
            slug = slugify(name)

            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            product = Product.objects.create(
                name=name,
                slug=slug,
                description=description,
                price=price,
                product_type=product_type,
                quantity=quantity,
                in_stock=in_stock
            )

            for i, img in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=img,
                    is_main=(i == 0)
                )

            messages.success(request, f'Товар "{name}" добавлен')
            return redirect(f'/admin-panel/?tab=products')

        elif 'edit_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)

            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = float(request.POST.get('price'))
            product.product_type_id = request.POST.get('product_type') or None
            product.quantity_id = request.POST.get('quantity') or None
            product.in_stock = request.POST.get('in_stock') == 'on'
            product.save()

            images = request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=product, image=img)

            messages.success(request, f'Товар "{product.name}" обновлен')
            return redirect(f'/admin-panel/?tab=products')

        elif 'delete_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product_name = product.name
            product.delete()
            messages.success(request, f'Товар "{product_name}" удален')
            return redirect(f'/admin-panel/?tab=products')

        elif 'add_quantity' in request.POST:
            quantity_value = request.POST.get('quantity_value')

            if quantity_value:
                Quantity.objects.create(value=int(quantity_value))
                messages.success(request, f'Количество "{quantity_value} ягод" добавлено')
                return redirect(f'/admin-panel/?tab=quantities')

        elif 'delete_quantity' in request.POST:
            quantity_id = request.POST.get('quantity_id')
            quantity = get_object_or_404(Quantity, id=quantity_id)
            quantity_value = quantity.value
            quantity.delete()
            messages.success(request, f'Количество "{quantity_value} ягод" удалено')
            return redirect(f'/admin-panel/?tab=quantities')

        return redirect(f'/admin-panel/?tab={active_tab}')

    context = {
        'products': products,
        'quantities': quantities,
        'types': types,
        'active_tab': active_tab,
    }
    return render(request, 'admin_panel/admin_dashboard.html', context)


@staff_member_required
def admin_orders(request):
    if not request.user.is_admin_user():
        return redirect('index')

    orders = Order.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status', '')

    if status_filter:
        orders = orders.filter(status=status_filter)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f'Статус заказа #{order.id} изменен')
        return redirect('admin_orders')

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'admin_panel/orders.html', context)


def get_product_data(request, product_id):
    if not request.user.is_admin_user():
        return JsonResponse({'error': 'Access denied'}, status=403)

    product = get_object_or_404(Product, id=product_id)
    images = [{'id': img.id, 'url': img.image.url} for img in product.images.all()]
    data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'product_type_id': product.product_type_id,
        'quantity_id': product.quantity_id,
        'in_stock': product.in_stock,
        'images': images,
    }
    return JsonResponse(data)


@csrf_exempt
def delete_product_image(request, image_id):
    if not request.user.is_admin_user():
        return JsonResponse({'error': 'Access denied'}, status=403)

    image = get_object_or_404(ProductImage, id=image_id)
    image.delete()
    return JsonResponse({'success': True})


def get_admin_notifications(request):
    if not request.user.is_admin_user():
        return JsonResponse({'error': 'Access denied'}, status=403)

    week_ago = timezone.now() - timedelta(days=7)
    new_orders = Order.objects.filter(created_at__gte=week_ago).order_by('-created_at')

    read_notifications = request.session.get('read_notifications', [])

    notifications = []
    for order in new_orders:
        diff = timezone.now() - order.created_at
        if diff.days > 0:
            time_ago = f'{diff.days} дн. назад'
        elif diff.seconds // 3600 > 0:
            time_ago = f'{diff.seconds // 3600} ч. назад'
        elif diff.seconds // 60 > 0:
            time_ago = f'{diff.seconds // 60} мин. назад'
        else:
            time_ago = 'только что'

        notifications.append({
            'order_id': order.id,
            'user_name': order.user.username,
            'read': order.id in read_notifications,
            'time_ago': time_ago,
        })

    return JsonResponse({'notifications': notifications})


def get_notifications_count(request):
    if not request.user.is_admin_user():
        return JsonResponse({'count': 0})

    week_ago = timezone.now() - timedelta(days=7)
    read_notifications = request.session.get('read_notifications', [])

    count = Order.objects.filter(created_at__gte=week_ago).exclude(id__in=read_notifications).count()
    return JsonResponse({'count': count})


def mark_notification_read(request, order_id):
    if not request.user.is_admin_user():
        return JsonResponse({'error': 'Access denied'}, status=403)

    read_notifications = request.session.get('read_notifications', [])
    if order_id not in read_notifications:
        read_notifications.append(order_id)
        request.session['read_notifications'] = read_notifications

    return JsonResponse({'success': True})


def mark_all_notifications_read(request):
    if not request.user.is_admin_user():
        return JsonResponse({'error': 'Access denied'}, status=403)

    week_ago = timezone.now() - timedelta(days=7)
    new_orders = Order.objects.filter(created_at__gte=week_ago)

    read_notifications = [order.id for order in new_orders]
    request.session['read_notifications'] = read_notifications

    return JsonResponse({'success': True})


def get_notifications_count(request):
    if not request.user.is_admin_user():
        return JsonResponse({'count': 0})

    week_ago = timezone.now() - timedelta(days=7)
    read_notifications = request.session.get('read_notifications', [])

    count = Order.objects.filter(created_at__gte=week_ago).exclude(id__in=read_notifications).count()
    return JsonResponse({'count': count})