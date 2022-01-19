# Generated by Django 3.2.9 on 2022-01-19 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='measurement',
        ),
        migrations.AddField(
            model_name='product',
            name='measurement_item',
            field=models.PositiveIntegerField(default=1, verbose_name='Չափման միավոր(հատ)'),
        ),
        migrations.AddField(
            model_name='product',
            name='measurement_kg',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Չափման միավոր(կգ)'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='delivery_cost',
            field=models.PositiveIntegerField(default=0, verbose_name='Առաքման արժեքը'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_cost',
            field=models.PositiveIntegerField(default=0, verbose_name='Առաքման արժեք'),
        ),
        migrations.AlterField(
            model_name='order',
            name='finale_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Ընդհանուր գումար'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Նկար'),
        ),
        migrations.AlterField(
            model_name='product',
            name='new_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Նոր գին'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Գին'),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Սկզբնական չափ'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Անուն'),
        ),
        migrations.AlterField(
            model_name='time_shipping',
            name='time_shipping',
            field=models.CharField(max_length=100, verbose_name='Առաքման ժամ'),
        ),
        migrations.DeleteModel(
            name='Measurement',
        ),
    ]
