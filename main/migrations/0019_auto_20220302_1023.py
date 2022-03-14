# Generated by Django 3.2.9 on 2022-03-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20220216_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Մեկնաբանություն'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Ակտիվ'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Մեկնաբանություն'),
        ),
    ]