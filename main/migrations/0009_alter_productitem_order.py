# Generated by Django 3.2.9 on 2022-02-04 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20220204_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.order', verbose_name='Պատվեր'),
        ),
    ]
