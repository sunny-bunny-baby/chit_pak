
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_review_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChocolateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_extra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraBerry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_extra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraFlower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_extra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PackagingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_extra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='extra_berries',
            field=models.TextField(blank=True, help_text='ID ягод через запятую'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='extra_flowers',
            field=models.TextField(blank=True, help_text='ID цветов через запятую'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='total_extra_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='extra_berries',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='extra_flowers',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='total_extra_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='chocolate_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.chocolatetype'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='chocolate_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.chocolatetype'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='packaging_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.packagingtype'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='packaging_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.packagingtype'),
        ),
    ]
