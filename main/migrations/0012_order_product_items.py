# Generated by Django 3.2.9 on 2022-02-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_order_product_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_items',
            field=models.ManyToManyField(to='main.ProductItem', verbose_name='Պատվերի ապրանքներ'),
        ),
    ]
