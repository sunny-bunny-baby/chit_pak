
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_product_category_remove_product_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='total_extra_price',
            new_name='extra_price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='extra_flowers',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='chocolate_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='flower_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='flower_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='packaging_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='chocolate_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='extra_berries',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='packaging_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
