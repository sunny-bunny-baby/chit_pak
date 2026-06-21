
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_cartitem_selected_quantity_option_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='reviews/'),
        ),
    ]
