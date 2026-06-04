from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm
from shop.models import Order, Review


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'auth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')

            new_password = request.POST.get('new_password')
            if new_password:
                if new_password == request.POST.get('confirm_password'):
                    user.set_password(new_password)
                else:
                    messages.error(request, 'Пароли не совпадают')

            user.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('profile')

        elif 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
            request.user.save()
            messages.success(request, 'Аватар обновлен')
            return redirect('profile')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
        'user_reviews': user_reviews,
    }
    return render(request, 'profile.html', context)