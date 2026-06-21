
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, choices=[('carton', 'Картон'), ('kraft', 'Крафт'), ('paper', 'Бумага'), ('textile', 'Текстиль')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, to='shop.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='shop.size'),
        ),
    ]
