# Generated by Django 3.2.9 on 2022-02-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20220205_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='wholesale',
            field=models.BooleanField(default=False, verbose_name='Մեծածախ'),
        ),
    ]