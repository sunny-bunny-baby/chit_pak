
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_color_size_product_material_product_colors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occasion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='material',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='selected_quantity_option',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='delivery_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='selected_quantity_option',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_options',
            field=models.CharField(blank=True, choices=[('5', '5 клубник'), ('7', '7 клубник'), ('9', '9 клубник'), ('12', '12 клубник'), ('15', '15 клубник'), ('21', '21 клубника'), ('25', '25 клубник'), ('31', '31 клубника'), ('51', '51 клубника'), ('101', '101 клубника')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'В обработке'), ('confirmed', 'Подтверждён'), ('preparing', 'Готовится'), ('ready', 'Готов к выдаче'), ('delivered', 'Доставлен'), ('cancelled', 'Отменён')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='occasion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.occasion'),
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
