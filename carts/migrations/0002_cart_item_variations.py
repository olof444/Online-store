# Generated by Django 4.0.3 on 2022-03-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_variations_options'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variations'),
        ),
    ]
