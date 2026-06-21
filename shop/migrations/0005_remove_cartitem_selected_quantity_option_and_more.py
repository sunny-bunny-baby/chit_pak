
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_occasion_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='selected_quantity_option',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='selected_quantity_option',
        ),
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity_options',
        ),
    ]
