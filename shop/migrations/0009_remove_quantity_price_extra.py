
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_quantity_alter_cartitem_extra_berries_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='price_extra',
        ),
    ]
