# Generated by Django 3.2.9 on 2022-01-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220119_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='quantity',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=10, verbose_name='Քանակ'),
        ),
    ]