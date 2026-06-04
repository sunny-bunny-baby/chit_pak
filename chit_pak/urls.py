from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views
from accounts import views as accounts_views
from admin_panel import views as admin_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', shop_views.index, name='index'),
                  path('catalog/', shop_views.catalog, name='catalog'),
                  path('about/', shop_views.about, name='about'),
                  path('product/<slug:product_slug>/', shop_views.product_detail, name='product_detail'),
                  path('add-to-cart/<int:product_id>/', shop_views.add_to_cart, name='add_to_cart'),
                  path('cart/', shop_views.cart, name='cart'),
                  path('cart/update/<int:item_id>/', shop_views.update_cart, name='update_cart'),
                  path('cart/remove/<int:item_id>/', shop_views.remove_from_cart, name='remove_from_cart'),
                  path('checkout/', shop_views.checkout, name='checkout'),
                  path('reviews/', shop_views.reviews, name='reviews'),
                  path('profile/', accounts_views.profile, name='profile'),
                  path('cart-count/', shop_views.get_cart_count, name='cart_count'),
                  path('order-details/<int:order_id>/', shop_views.order_details, name='order_details'),

                  path('login/', accounts_views.login_view, name='login'),
                  path('register/', accounts_views.register_view, name='register'),
                  path('logout/', accounts_views.logout_view, name='logout'),

                  path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
                  path('admin-panel/orders/', admin_views.admin_orders, name='admin_orders'),
                  path('admin/notifications/', admin_views.get_admin_notifications, name='admin_notifications'),
                  path('admin/notifications/count/', admin_views.get_notifications_count, name='notifications_count'),
                  path('admin/notification/read/<int:order_id>/', admin_views.mark_notification_read,
                       name='mark_notification_read'),
                  path('admin/notifications/mark-all-read/', admin_views.mark_all_notifications_read,
                       name='mark_all_read'),
                    path('admin-panel/get-product/<int:product_id>/', admin_views.get_product_data, name='get_product_data'),
                    path('admin-panel/delete-image/<int:image_id>/', admin_views.delete_product_image, name='delete_product_image'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)