from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, Quantity, Type, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)
    extra = 3

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Просмотр'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'product_type', 'quantity', 'in_stock', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('product_type', 'quantity', 'in_stock', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'in_stock')
    inlines = [ProductImageInline]
    readonly_fields = ('get_main_image_preview',)

    def get_main_image_preview(self, obj):
        main_image = obj.get_main_image()
        if main_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', main_image)
        return "Нет главного изображения"

    get_main_image_preview.short_description = 'Главное изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    search_fields = ('value',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(ProductImage)