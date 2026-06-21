
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_chocolatetype_extraberry_extraflower_packagingtype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(unique=True)),
                ('price_extra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='extra_berries',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='extra_flowers',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.quantity'),
        ),
    ]
