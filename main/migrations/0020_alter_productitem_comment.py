# Generated by Django 3.2.9 on 2022-03-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20220302_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Մեկնաբանություն'),
        ),
    ]
