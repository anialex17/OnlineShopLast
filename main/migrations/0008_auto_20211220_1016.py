# Generated by Django 3.2.9 on 2021-12-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_productitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='Կատեգորիա'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_hy',
            field=models.CharField(max_length=250, null=True, verbose_name='Կատեգորիա'),
        ),
        migrations.AddField(
            model_name='category',
            name='title_ru',
            field=models.CharField(max_length=250, null=True, verbose_name='Կատեգորիա'),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_en',
            field=models.TextField(blank=True, null=True, verbose_name='Հասցե'),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_hy',
            field=models.TextField(blank=True, null=True, verbose_name='Հասցե'),
        ),
        migrations.AddField(
            model_name='customer',
            name='address_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Հասցե'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_hy',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_hy',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_hy',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
