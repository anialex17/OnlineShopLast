# Generated by Django 3.2.9 on 2022-02-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_productitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='product_items',
            field=models.ManyToManyField(to='main.ProductItem', verbose_name='Պատվերի ապրանքներ'),
        ),
    ]
