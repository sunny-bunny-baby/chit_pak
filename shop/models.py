from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Quantity(models.Model):
    value = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.value} ягод"


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(Type, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    quantity = models.ForeignKey(Quantity, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_main_image(self):
        main = self.images.filter(is_main=True).first()
        if main:
            return main.image.url
        first = self.images.first()
        if first:
            return first.image.url
        return None

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Изображение для {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    chocolate_type = models.CharField(max_length=50, blank=True, null=True)
    chocolate_color = models.CharField(max_length=50, blank=True, null=True)
    packaging_type = models.CharField(max_length=50, blank=True, null=True)
    packaging_color = models.CharField(max_length=50, blank=True, null=True)
    extra_berries = models.CharField(max_length=200, blank=True, null=True)
    flower_type = models.CharField(max_length=50, blank=True, null=True)
    flower_color = models.CharField(max_length=50, blank=True, null=True)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_total_price(self):
        return (self.product.price + self.extra_price) * self.quantity


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('confirmed', 'Подтверждён'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов к выдаче'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    comment = models.TextField(blank=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    chocolate_type = models.CharField(max_length=50, blank=True, null=True)
    chocolate_color = models.CharField(max_length=50, blank=True, null=True)
    packaging_type = models.CharField(max_length=50, blank=True, null=True)
    packaging_color = models.CharField(max_length=50, blank=True, null=True)
    extra_berries = models.CharField(max_length=200, blank=True, null=True)
    flower_type = models.CharField(max_length=50, blank=True, null=True)
    flower_color = models.CharField(max_length=50, blank=True, null=True)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_total_price(self):
        return (self.price + self.extra_price) * self.quantity


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Отзыв от {self.user.username}"